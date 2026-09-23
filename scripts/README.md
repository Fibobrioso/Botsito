# scripts/
Operaciones puntuales sin logica de negocio (llaman al paquete botsito o a git).

- `git-hooks/`: hooks versionados (ADR-0003). `pre-commit` rechaza commits en `main`, ediciones de
  `knowledge/evidence`, `knowledge/feedback`, `data/manifests`, `knowledge/corpus/transcripciones` y
  `knowledge/corpus/fotogramas`,
  `uv.lock` desactualizado y contratos de importacion rotos.
- `instalar_hooks.py`: copia los hooks al directorio de hooks del repositorio (`make hooks`).
  Portable (Python, sin `cp`/`chmod`); aborta si `core.hooksPath` esta configurado fuera del repo.
- `decodificar_png.py`: decodificador de PNG de biblioteca estandar (`zlib` y `struct`), HERRAMIENTA
  DE MEDIDA de fotogramas, fuera del paquete; su test fabrica sus propios PNG con los cinco filtros
  (`tests/unit/test_decodificar_png.py`). Next Action 4, 2026-09-23.
- Futuro: grabacion de ticks de la demo (F17), exportacion de FXReplay (F26). La transcripcion de
  un video es un comando del paquete (`botsito corpus transcribe`, F04), no un script.
