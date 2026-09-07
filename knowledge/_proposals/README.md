# knowledge/_proposals/ — propuestas de evidencia (F07, ADR-0009)

Registro de lo que un proponente (un LLM o una persona) propuso como evidencia sobre un tramo de
la cruda: prompt integro, modelo, contexto (segmentos de la cruda y referencias de fotogramas del
tramo), salida (`items` y `no_consta`) y decision humana por item. Es la pista de auditoria que
exige la seccion H del plan ("prompt, modelo, salida y decision humana"). El proponente NUNCA
escribe en `knowledge/evidence/`: solo `botsito evidence accept` crea un item, y lo hace con todas
las comprobaciones de `evidence new` (cita localizada en la cruda, fotograma real, transcripcion
activa).

## Regimen
Manual y versionado (no inmutable, no solo-anadir). Tras `botsito evidence propose --check`, la
salida queda sellada con `salida_sha256`; a partir de ahi solo pueden cambiar los campos de
decision de cada item (`decision`, `decidido_por`, `decidido_el`, `metodo_revision`, `motivo`,
`evidence_id`). `knowledge validate` recomputa el sello de cada propuesta y exige que todo
`evidence_id` anotado exista. Una salida que cambio despues del check es error: se crea otra
propuesta.

## Flujo
```
botsito evidence propose --video v4 --t0 0:05:00 --t1 0:15:00 --modelo <quien> --tema-buscado stop ...
   -> knowledge/_proposals/pr-v4-000500-001500-<hash8>.yaml (esqueleto: contexto + prompt + items: [])
(el proponente rellena `items` y `no_consta` a mano o por API)
botsito evidence propose --check knowledge/_proposals/pr-....yaml       # guardias + sello
botsito evidence accept --propuesta <fichero> --item 3 --revisado-por "<persona> · hoja F07 <fecha> · cruda leida" --metodo cruda_leida
botsito evidence reject --propuesta <fichero> --item 4 --motivo "..." --decidido-por "<persona>"
```

## Esquema del fichero
`propuesta_id` (`pr-<video>-<t0hhmmss>-<t1hhmmss>-<hash8>`), `video_id`, `transcripcion` (id
`tr-*` de la cruda), `t0`, `t1`, `prompt`, `prompt_sha256`, `modelo`, `proponente` (`llm` |
`humano`), `generado_el`, `contexto` (`segmentos` con `n`, `t0_ms`, `t1_ms`, `texto`, `senales`;
`referencias` `fr-*` del tramo), `temas_buscados`, `items`, `no_consta` (`[{tema, motivo}]`),
`salida_sha256`, `comprobado_el`, `notas`.

Cada item: `n`, `t0`, `t1`, `modalidad`, `tipo`, `cita_literal` (copiada de la CRUDA; comodin
`[...]` para omitir palabras, maximo 2), `afirmacion`, `tema` (raiz en
`knowledge/evidence/_temas.yaml`), `valor` (solo una cifra presente en la cita o un valor
cerrado), `confianza`, `fotogramas` (`fr-<id>/<t_ms>` del tramo; `material_adicional` solo
acompanado de un `fr-*`), `notas`, `marca_heredada` (si re-cita una marca de la investigacion
previa: el item saldra con `provenance: bot-v2`), y los campos de decision.

## Guardias de `--check`
Cita localizada por tokens en la cruda dentro de `[t0 - 2 s, t1 + 2 s]` y con tiempo real por
palabras; cita >= 4 tokens; tema en la taxonomia; `valor` presente en la cita; dos items con la
misma cita (en cualquier propuesta o en la evidencia) = error; mismo tema con localizaciones
solapadas = error; cita en un segmento con senales del ASR o con duda del glosario => la
confianza no puede ser `alta`; cada `tema_buscado` aparece en `items` o en `no_consta`; una cita
igual rechazada en otra propuesta = aviso.

`PROMPT.md` es el prompt canonico del proponente; su sha256 va en cada propuesta y solo cambia
con commit (una propuesta con otro prompt se marca con AVISO en `knowledge validate`).
