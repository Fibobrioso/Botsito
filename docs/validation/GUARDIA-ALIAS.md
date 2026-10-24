# GUARDIA-ALIAS · la guardia niega el material protegido escriba como se escriba la ruta

Rama: `trabajo/guardia-alias`, abierta el 2026-10-24 desde `main` en `af89a78` (commit de estado
sobre el merge `2cc3b93`, tag `stable/F38b-guardia-ci`). Encargo:
`docs/encargos/trabajo-guardia-alias.md`. Carril de guardias y deuda, G.1 de la hoja de ruta: paga
la línea PRIORITARIA de G.1 y la parte de K de la Next Action que habla del alias de la raíz en
`motivo_fichero` (lo que queda de K sigue en K). Tag de cierre previsto: `stable/F38c-guardia-alias`;
la ingesta de la sesión 5 pasa a F38d.

## Base comprobada al abrir

- `git fetch origin`; `git status --short` vacío en `main`.
- `git rev-parse main origin/main`: `af89a78802af71692221bcc941745d09330d4493` las dos veces.
- `git rev-parse main^1` = `git rev-parse "stable/F38b-guardia-ci^{commit}"` =
  `2cc3b93b68eb662d993146a2a5c819bf4b45f6d4`; el tag está en origin
  (`git ls-remote --tags origin stable/F38b-guardia-ci`:
  `47d20ceae55cfe6575b4759a41209814c4179819 refs/tags/stable/F38b-guardia-ci`, el objeto del tag
  anotado). La última línea `- Tag:` de HISTORIA nombra ese mismo tag.
- CI de `main` sobre su HEAD, con una consulta suelta (`gh run view 40092378098 --json
  headSha,status,conclusion,event,headBranch`): `completed` / `success`, `headSha` `af89a78…`,
  rama `main`, evento `push`.
- `git branch --list` solo da `main`; `git ls-remote --heads origin` solo da `refs/heads/main`.
- `Current Feature` no está en WAITING_FOR_USER_VALIDATION.
- La carpeta del diagnóstico del 2026-10-24 existe en el scratchpad de la sesión anterior
  (`…\49e8894b-c04f-4137-9483-9024a98edd2b\scratchpad\diagK\`) con los cinco ficheros que nombra el
  encargo (DIAGNOSTICO-K.md, tabla.md, medir_k.py, existe.py, contar.py), más una subcarpeta
  `Bot v3 prueba` y un `errores.txt` vacío. Solo listada; su contenido se revisa en la fase 0.a.

## Estado

EN CURSO: rama abierta; falta la fase 0.
