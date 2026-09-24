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
- `v5_criterio.py`: el criterio de lectura de los seis instantes de v5, CONGELADO antes de mirar
  (`docs/validation/V5-INSTANTES-CRITERIO.md`). `--calibrar` lee solo los cuatro fotogramas ya
  abiertos; `--medir` lee los 36 de la ventana fija y no se ejecuta sin luz verde del consultor.
- `a18_buscar.py`: la busqueda de A-18 en las transcripciones vigentes de v1 a v5, CONGELADA antes de ejecutarla
  (`docs/validation/A18-TRANSCRIPCIONES-CRITERIO.md`): 36 terminos, ventana de +-45 s, solo la cruda
  verificada contra su manifiesto. Se ejecuta una sola vez.
- `instante_llenado.py`: si el instante del xlsx es el LLENADO o la COLOCACION de la orden, con
  control a -30 y +30 min (`docs/validation/CRITERIO-FIDELIDAD.md` §1). Solo imprime tasas.
- `sesgo_h4_diagnostico.py`: DIAGNOSTICO del sesgo H4 sobre abril y agosto (construccion), sin
  umbral y sin tocar mayo (`docs/validation/MOTOR-SESGO-H4.md`). Solo imprime recuentos.
- `buscar_ambiguedades.py`: la busqueda de A-24, A-21, A-26 y A-34 en las transcripciones, CONGELADA
  antes de ejecutarla (`docs/validation/A24-A21-A26-A34-CRITERIO.md`): terminos por ambiguedad,
  ventana de +-45 s y pasajes de como mucho 180 s. Reutiliza `a18_buscar.py`. Con `--conjunto a35`,
  la de A-35 con su propia lista cerrada (`docs/validation/A35-PIVOTE-FORMADO-CRITERIO.md`).
- Futuro: grabacion de ticks de la demo (F17), exportacion de FXReplay (F26). La transcripcion de
  un video es un comando del paquete (`botsito corpus transcribe`, F04), no un script.
