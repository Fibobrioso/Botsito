# scripts/
Operaciones puntuales sin logica de negocio (llaman al paquete botsito o a git).

- `git-hooks/`: hooks versionados (ADR-0003). `pre-commit` rechaza commits en `main`, ediciones de
  `knowledge/evidence`, `knowledge/feedback`, `data/manifests`, `knowledge/corpus/transcripciones` y
  `knowledge/corpus/fotogramas`,
  `uv.lock` desactualizado y contratos de importacion rotos.
- `instalar_hooks.py`: copia los hooks al directorio de hooks del repositorio (`make hooks`).
  Portable (Python, sin `cp`/`chmod`); aborta si `core.hooksPath` esta configurado fuera del repo.
- `mover_sesion.py`: cambia la fecha de una sesion del kit sin cambiar nada mas (F10, ADR-0011). El
  seed no se teclea: se lee del paquete que ya existe, y si los casos o su reparto salen distintos
  restaura el original. Su uso lo explica `knowledge/cases/kit/README.md` («Si cambia la fecha de
  la sesion»).
- `sello_make_check.py`: el sello de `make check` (rama `trabajo/blindaje`). `borrar` al empezar y
  `sellar` al terminar en verde: escribe el hash del arbol estadiado dentro del directorio de git,
  salvo que haya cambios sin estadiar o ficheros sin seguir. Los hooks `pre-commit` y
  `pre-merge-commit` rechazan un arbol sin ese sello (`scripts/git-hooks/README.md`).
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
- `huso_por_velas.py`: el huso de un libro del trader MEDIDO POR VELAS, el procedimiento de
  ADR-0039 §5 hecho herramienta (2026-09-24, ADR-0046 §6c). Todas sus cifras y sus husos salen de
  `knowledge/corpus/criterio_huso.yaml`; los dias `dev`, de los repartos commiteados. Con un libro
  ya declarado es CONTROL, y si no coincide sale con codigo 3. Solo imprime recuentos y tasas
  (control de abril: `docs/validation/HUSO-POR-VELAS-CONTROL-ABRIL.txt`).
- `sesgo_h4_diagnostico.py`: DIAGNOSTICO del sesgo H4 sobre abril y agosto (construccion), sin
  umbral y sin tocar mayo (`docs/validation/MOTOR-SESGO-H4.md`). Solo imprime recuentos.
- `buscar_ambiguedades.py`: la busqueda de A-24, A-21, A-26 y A-34 en las transcripciones, CONGELADA
  antes de ejecutarla (`docs/validation/A24-A21-A26-A34-CRITERIO.md`): terminos por ambiguedad,
  ventana de +-45 s y pasajes de como mucho 180 s. Reutiliza `a18_buscar.py`. Con `--conjunto a35`,
  la de A-35 con su propia lista cerrada (`docs/validation/A35-PIVOTE-FORMADO-CRITERIO.md`).
  Con `--conjunto sesion02`, la de los candidatos C-01, C-02, C-04, C-05, C-06 y C-07 de la
  sesion 02 (`docs/validation/SESION-02-BUSQUEDA-CRITERIO.md`).
- `hoja_preguntas.py`: la hoja en Word de una sesion SOLO DE PREGUNTAS, desde
  `knowledge/spec/ambiguedades.yaml`, en el orden que fijo el consultor para la sesion 02
  (`ORDEN_SESION_02`). Escribe `hoja-sesion-02.docx` en la raiz, que no se versiona
  (`docs/runbooks/SESION-DE-PREGUNTAS.md`). Una pregunta ya cerrada hace fallar la hoja.
- `a35_fotogramas.py`: los fotogramas de A-35, CONGELADOS antes de abrir ninguno
  (`docs/validation/A35-FOTOGRAMAS-CRITERIO.md`): lista cerrada por ventana de segmento,
  verificacion contra la extraccion de F05 y pixeles distintos del anterior; no lee el grafico.
- Futuro: grabacion de ticks de la demo (F17), exportacion de FXReplay (F26). La transcripcion de
  un video es un comando del paquete (`botsito corpus transcribe`, F04), no un script.
