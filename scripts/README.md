# scripts/
Operaciones puntuales sin logica de negocio (llaman al paquete botsito o a git).

- `git-hooks/`: hooks versionados (ADR-0003). `pre-commit` rechaza commits en `main`, ediciones de
  evidencia o feedback y contratos de importacion rotos.
- `instalar_hooks.py`: copia los hooks al directorio de hooks del repositorio (`make hooks`).
  Portable (Python, sin `cp`/`chmod`); aborta si `core.hooksPath` esta configurado fuera del repo.
- Futuro: ingesta de un video (F04), grabacion de ticks de la demo (F17), exportacion de FXReplay
  (F26).
