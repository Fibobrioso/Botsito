# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** T · el vídeo de julio (v11-v14): transcripción, fotogramas, cobertura por día y comparación con el libro (R2.4)
**Rama:** trabajo/video-julio
**Objetivo:** oír al trader sobre julio: transcribir v11 a v14, comprobar qué días cubre cada vídeo, comparar el vídeo con los casos del libro de julio (días 1 a 17) y preparar la clasificación de las 81 filas «sin clase hasta T» y el inventario de los días 20 a 31 (encargo en `docs/encargos/trabajo-video-julio.md`).

## Base (comprobada con git al abrir, 2026-11-08)

- `git rev-parse main origin/main`: `5a54b468a4de3a0f36124cdac0da481d4abf2ed4` las dos veces.
- Último `- Tag:` de HISTORIA: `stable/F38t-recorrida-construccion-2`; `git rev-parse "stable/F38t-recorrida-construccion-2^{commit}"` = `git rev-parse main^1` = `86f306a0dc577eb78de673b45f923d5ef89a434b`; en origin (`git ls-remote --tags`: `4e20ad1…` refs/tags/stable/F38t-recorrida-construccion-2).
- CI de main sobre `5a54b468a4de3a0f36124cdac0da481d4abf2ed4` (check-runs): `Python completed success`, run 42550658681.
- `git branch --list`: solo `main`; `git ls-remote --heads origin`: solo `refs/heads/main`.

## Fase 0

EN CURSO.

## Estado
EN CURSO
