---
status: ACTIVE
date: 2026-09-07
phase: F07
---

# 0009 · Verificacion mecanica de citas y propuestas de evidencia trazables

## Decision
1. **Cita de audio atada a la cruda y al tiempo.** `EvidenceItem` gana el campo opcional
   `transcripcion` (id `tr-*`); `modalidad: audio | ambas` lo exige (debe ser la transcripcion
   activa del video al crear el item) y `pantalla` lo prohibe. La `cita_literal` se localiza POR
   TOKENS (NFC, `casefold`, numeros con separador interior como un token: `0.75`, `16,5`, `1:3`;
   guiones y apostrofes como espacio; acentos conservados; los `...` del ASR se eliminan) dentro
   de los segmentos de la cruda que tocan `[t0 - 2 s, t1 + 2 s]`, con el comodin `[...]` (maximo
   2, trozos >= 3 tokens, cita >= 4 tokens), y su tiempo real se lee de las `palabras`
   (alineadas por caracteres sin espacios); ese tiempo debe caer en la ventana. `knowledge
   validate` verifica SIEMPRE contra la cruda citada (inmutable; en `data/` y en Drive), nunca
   contra "la activa del momento": una retranscripcion no invalida items que nadie edito; si la
   transcripcion citada quedo reemplazada, un aviso agregado por transcripcion dice cuantos
   items la citan y cuantos se localizan tambien en la nueva (F08/F11 deciden re-citar).
2. **Cita de pantalla atada a un fotograma real.** `modalidad: pantalla | ambas` exige al menos
   una referencia `fr-<id>/<t_ms>` del mismo video con `t_ms` en `[t0 - 1 s, t1 + 1 s]` y
   presente en `referencias_conocidas` (ADR-0008 §6); `audio` no admite `fotogramas`; una ruta
   `material_adicional` solo se cita acompanada de un `fr-*` del tramo que la muestra. Lo que
   dice la cita de pantalla lo afirma la persona que la acepta (`fotograma visto`).
3. **`evidence` no importa `corpus`.** La verificacion vive en `evidence/verificacion.py` sobre
   un protocolo estructural (`SegmentoCitable`, `PalabraCitable`); `validation/contexto_evidencia.py`
   compone crudas, referencias, transcripciones activas y reemplazos en un `ContextoEvidencia`
   que consumen `validar_contra_manifiesto`, `verificar_citas` y `propuestas.comprobar`.
4. **Propuestas trazables** en `knowledge/_proposals/pr-<video>-<t0>-<t1>-<hash8>.yaml`: prompt
   integro y su sha256, modelo, proponente (`llm` | `humano`), contexto del tramo (segmentos sin
   `palabras`, referencias), `temas_buscados`, `items` y `no_consta`. Regimen manual y versionado;
   tras `propose --check` la salida queda sellada (`salida_sha256`) y solo cambian los campos de
   decision. El proponente nunca escribe en `knowledge/evidence/`; `evidence accept` crea el
   item con `extractor` = proponente, `revisado_por` = "<persona> · hoja F07 <fecha> · cruda
   leida | fotograma visto" y `provenance: bot-v2` solo si la propuesta declara `marca_heredada`.
5. **Guardias de calidad** (en `--check` y `accept`): cita >= 4 tokens; `tema` con raiz en
   `knowledge/evidence/_temas.yaml`; `valor` presente en la cita o en los valores cerrados; misma
   cita normalizada en dos items (propuestas o evidencia) = error; mismo tema con localizaciones
   solapadas = error; cita en un segmento con senales del ASR o con duda del glosario => la
   confianza no puede ser `alta`; cada `tema_buscado` aparece en `items` o en `no_consta`.
6. **`revisado_por` redefinido**: quien acepto el item y con que metodo. La cita de audio la
   verifica la maquina; la persona revisa que `afirmacion`, `tema` y `valor` no digan mas que la
   cita, y en pantalla que el fotograma muestre lo citado.

## Problema que resuelve
F06 aceptaba cualquier `cita_literal` de 5 caracteres y cualquier ruta del manifiesto como
fotograma: una cita podia ser una parafrasis o apuntar a un tramo donde no se dice. La seccion H
exige "sin inferencias" y "propuestas con prompt, modelo, salida y decision": sin verificacion
mecanica ni registro de propuestas, la base de conocimiento arrancaria contaminada.

## Alternativas consideradas
1. Comparar por subcadena normalizada (no por tokens). 2. Comodin ` ... ` (elipsis). 3. Verificar
contra la transcripcion activa del momento. 4. Propuestas inmutables o solo-anadir. 5. Un cliente
de API de LLM como proponente.

## Por que elegimos esta opcion
Por tokens, `3` no casa dentro de `33` ni `1.3` dentro de `11.3`; el ASR ya escribe `...`, asi
que el comodin debe ser otro; la cruda citada es inmutable y esta respaldada, y verificar contra
otra invalidaria items que nadie edito; las propuestas necesitan anotar la decision humana en el
mismo fichero, asi que el sello de la salida es lo que las hace trazables; no hay clave de API y
el formato de propuesta es la interfaz (esta sesion de Claude Code propone; una API rellenaria el
mismo esqueleto).

## Por que descartamos las demas
(1) deja pasar coincidencias parciales de numeros; (2) confunde el comodin con la puntuacion del
ASR (medido: v2 8, v3 11, v4 6 segmentos con `...`); (3) rompe "100 % verificadas" por deriva
entre transcripciones; (4) impide anotar la decision sin duplicar ficheros; (5) no hay clave y
anadiria una dependencia sin uso.

## Impacto
`src/botsito/evidence/{modelo,verificacion,propuestas}.py`, `src/botsito/validation/{knowledge,
contexto_evidencia}.py`, `src/botsito/cli.py` (`evidence new --transcripcion | propose | accept |
reject | list`), `src/botsito/comun/ids.py` (`pr-*`), `knowledge/evidence/{README.md,_temas.yaml}`,
`knowledge/_proposals/{README.md,PROMPT.md}`, `knowledge/README.md`, tests. Los items de F06 no
existian; ningun id cambia. `test_import_contracts` prohibe `evidence -> corpus`.

## Enmienda 2026-09-08 (F08, ADR-0010)
§3: quienes componen crudas, referencias y evidencia son `validation` (contexto de verificacion) y
`retrieval` (indice de busqueda); lo que es del corpus (`dudas_de`, `cargar_capas`) vive en
`corpus.pipeline_transcripcion`. `buscar_secuencia` (todas las apariciones, sin minimos) es la
base de `localizar_cita`, que conserva sus minimos y su ventana.

## Enmienda 2026-09-07 (auditoria de cierre de F07)
- `localizar_cita` prueba TODAS las apariciones del primer trozo dentro de la ventana y se
  queda con la primera aparicion completa que cabe en `[t0 - 2 s, t1 + 2 s]`; `coincidencias`
  cuenta las apariciones completas que caben (antes, una frase repetida en un segmento que
  solo tocaba la ventana hacia fallar una cita verdadera).
- `Localizacion.hueco_ms`: mayor salto entre trozos consecutivos de una cita con comodin.
  `propose --check` AVISA a partir de 15 s (`HUECO_AVISO_MS`); no es error: el revisor humano
  decide si los trozos son una misma frase. De los 341 items aceptados, 41 tienen huecos de
  15 a 44 s; el usuario los acepto leyendo la cruda del tramo.
- Palabras incompletas al final de un segmento (el ASR omite la ultima palabra en `palabras`;
  5 segmentos en las crudas activas): se alinea lo que hay y los tokens restantes llevan el
  tramo `[fin de la ultima palabra, fin del segmento]`, con aviso `tiempos parciales`;
  `knowledge validate` imprime el recuento agregado de citas con tiempos de segmento o
  parciales (hoy 1: `ev-v3-000058-7b5ce480`).
- El sello `salida_sha256` cubre tambien la cabecera que decide la evidencia: `video_id`,
  `transcripcion`, `t0`, `t1`, `proponente` (las 20 propuestas se re-sellaron; decisiones y
  `comprobado_el` intactos).
- `knowledge validate` cruza cada decision con la evidencia: un `aceptado` anota un
  `evidence_id` existente y unico cuyos campos (cita, afirmacion, tema, valor, modalidad, tipo,
  t0/t1, confianza, fotogramas, `extractor` = `proponente`, `transcripcion`, `provenance`)
  son los del item propuesto, con `metodo_revision` coherente con la modalidad (pantalla/ambas
  exige `fotograma_visto`; audio exige `cruda_leida` o `audio_oido`); un rechazado o pendiente
  no puede anotar `evidence_id`; evidencia `extractor: llm` sin propuesta que la respalde es
  aviso.
- `evidence accept` retira el item recien creado si no puede anotar la decision en la
  propuesta; re-evalua cualquier problema del check que mencione el item (tambien los solapes);
  sin `manifest.yaml`, las referencias de pantalla se comprueban igual. Una cabecera de
  propuesta con tiempo invalido es `PropuestaError`, no traceback.
- Fuera de F07 (para F11): `_contradicciones.yaml` agrupa por `tema` exacto; el mismo parametro
  vive hoy bajo temas distintos elegidos por el proponente (`stop.nivel`, `stop.075_suficiente`,
  `stop.introducido_en_operacion_075`...; `cartuchos.*` con `dos`/`2`/`3`/`tres`), asi que "1
  contradiccion abierta" depende de esa granularidad. La taxonomia normativa de F11 decide
  que temas comparten parametro.

## Fecha / fase
2026-09-07 · F07

## Estado
ACTIVE
