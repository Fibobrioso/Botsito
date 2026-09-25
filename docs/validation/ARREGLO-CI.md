# Arreglo de la CI: main y el tag en un solo push atómico

Rama `trabajo/arreglo-ci`, 2026-09-25. Sin merge, sin tag y sin push.

## Qué pasó

El run `36174003223`, sobre `ac4e3a0` (el `docs(state)` de `trabajo/blindaje`), salió **rojo** en el
paso `make check` con «Process completed with exit code 2» (anotación del run, línea 91). En el
segundo intento, **sin cambiar el árbol**, salió verde (`run_attempt: 2`).

## Diagnóstico

**La carrera entre los dos pushes.** El ritual reescrito en `trabajo/blindaje` empujaba `main` y el
tag en dos líneas. Horas del run, de la API pública de GitHub:
- **18:31:45**, se crea el run con el push de `main`;
- **18:31:50**, la CI ejecuta `git fetch --tags --force`, cinco segundos después;
- el tag se empujó después, con otra línea.

Sin el tag nuevo, el último tag estable que ve la CI es el anterior, y `state check` falla.
Reproducido en un clon desechable de `ac4e3a0`, sin `stable/F14-blindaje`:

```
ERROR: 'Last Stable Commit' dice '8c6354e'; el tag stable/F19-sesion-02-preparada apunta a bd56fb4
ERROR: main tiene cambios sin tag estable desde stable/F19-sesion-02-preparada: .gitignore, CLAUDE.md, Makefile, …
```

Con el tag en su sitio, `OK`. **En local pasaba** porque el tag ya existía cuando corrió `make check`.

**Hipótesis descartadas, medidas:**
- el bit de ejecución: los dos hooks están en `100755`, en el índice y en `ac4e3a0`;
- la identidad de git: tampoco hay identidad global en local, y los tests la fijan en cada repo
  temporal.

**El log literal del run no se leyó.** Pide autenticación (403), y la extensión de Chrome no estaba
conectada. El diagnóstico se apoya en la reproducción, en las horas y en el segundo intento verde.

## El arreglo

- **`docs/runbooks/RITUAL.md`**: un solo `git push --atomic origin main stable/<tag>`, que actualiza
  los dos refs de una vez o ninguno, con la corrección 8, que cuenta el porqué. Comprobado en un
  remoto `bare` temporal: la rama y el tag anotado llegan en el mismo push. Ningún otro runbook
  empuja.
- **`tests/unit/test_push_atomico.py`**:
  - el fallo reproducido en un repo temporal: `state check` sobre un merge sin su tag falla con
    «main tiene cambios sin tag estable», y el mismo árbol pasa al crear el tag;
  - el ritual empuja una sola vez, con `--atomic`, `main` y el tag;
  - ningún runbook empuja `main` o un tag por separado;
  - la prueba de que el detector caza el ritual viejo.

## Estado

WAITING_FOR_USER_VALIDATION. El cierre de esta rama ya usa el push atómico.
