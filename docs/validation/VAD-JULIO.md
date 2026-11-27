# VAD-JULIO · La voz que el VAD del ASR se salta en v12 a v14 (R2.5, letra C)

> PLANTILLA: informe de la rama `trabajo/vad-julio`. Estado: EN CURSO. La fase 0, el criterio de
> D3 (copiado antes de las corridas), la tabla de candidatas, D4 por vídeo, D5, las desviaciones,
> las comprobaciones, la PARADA final, las líneas del cierre y el informe del revisor se escriben
> aquí según avanza la rama.

Rama `trabajo/vad-julio`, abierta el 2026-11-27 desde `main` en 139800f5 (commit de estado sobre
el merge d44f3e58 del tag `stable/F39r-renovar-cierres-2026-11-26`). Encargo:
`docs/encargos/trabajo-vad-julio.md`. Tramo: R2 (R2.5 de `docs/plan/HOJA-DE-RUTA.md`; la letra C
de la Next Action).

## La base, comprobada al abrir (skill `abrir-rama`, paso 1)

- `git rev-parse main origin/main`: `139800f5c860e0ae32d6dff9c3f836b7359848ca` dos veces.
- `git rev-parse "stable/F39r-renovar-cierres-2026-11-26^{commit}"` = `git rev-parse main^1` =
  `d44f3e58712f58bdbc2207f93f4cc4fb3acea857`; el tag está en origin (`git ls-remote --tags`).
  Es el último tag (`git tag --sort=-creatordate`: F39r, F39q, F39p).
- CI de `main` sobre `139800f5…`: check-run `python`, `completed` / `success`, run 46066643655
  (el que citaba el encargo).
- `git branch --list`: solo `main`; `git ls-remote --heads origin "fix/*"`: vacío.
- 0.1, antes de la fila del día: `casos_reservados(repo)` da 34 casos reservados, ninguno de
  2026-07 (los ids son `caso-eurusd-AAAA-MM-DD`).
