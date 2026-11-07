# SELLO-RESPALDO-M1 · la marca de _peor_del_minuto y los eventos que el respaldo M1 sella en el cierre de su vela

Rama `trabajo/sello-respaldo-m1`, abierta el 2026-11-07 desde `main` (2e04b63, commit de estado
sobre el merge 8f43d38 del tag `stable/F38p-demo-ejecuciones-2-3`). Encargo:
`docs/encargos/trabajo-sello-respaldo-m1.md`. Tramo «R3 · Una corrida del arnés sobre toda la
construcción» (R3.6 de la hoja de ruta; H de la Next Action).

## Base comprobada al abrir (2026-11-07)

- `git rev-parse main origin/main`: `2e04b632b81df9d702939626dbe26afdf1b7beea` las dos veces; su
  asunto es `docs(state): trabajo/demo-ejecuciones-2-3, cerrada en main (stable/F38p-demo-ejecuciones-2-3)`.
- `git rev-parse main^1` = `git rev-parse "stable/F38p-demo-ejecuciones-2-3^{commit}"` =
  `8f43d381a50a0466c31aea13401323c0eeb37ae5`; el tag esta en origin (`git ls-remote --tags`), y es
  la ultima linea `- Tag: ` de `docs/state/HISTORIA.md`.
- CI de `main` sobre su HEAD: `gh run view 42342344212` → `completed` / `success`, headSha
  `2e04b632b81df9d702939626dbe26afdf1b7beea`, rama `main`, workflow `ci`.
- `git branch -a` solo daba `main` y `origin/main`; `git ls-remote --heads origin` solo `main`.

## Estado

EN CURSO: rama abierta; la fase 0 la escribe el commit siguiente.
