---
name: comparar-con-main
description: Compara byte a byte la salida de main y la de la rama de Bot v3 (kit, fidelidad, ventanas y lo que el encargo nombre) en dos clones desechables con git worktree --detach, leyendo las velas del data/ real sin copiarlas ni descargarlas, y enseña por hash lo que coincide y por diff lo que difiere a proposito. Usala cuando un encargo pide una regresion contra main, «identico byte a byte», o probar algo «con el codigo de main».
argument-hint: "<rama> <lo que se compara>"
---

# comparar-con-main

Una regresion sin clones desechables ensucia el repo o compara cosas distintas. Las reglas viven en
`CLAUDE.md` («Ensayos aislados, y nada escribe mientras corre make check» y «Que se puede mirar y
que no»); aqui solo el orden y las puertas. Si discrepan, ganan ellos y se dice.

## Entradas

| Entrada | De donde sale | Si falta |
|---|---|---|
| Que se compara: los comandos exactos, con `uv run` y todos sus flags | el encargo o la respuesta a la PARADA | se pregunta |
| El universo (meses o dias) | el encargo; comprobado con `casos_reservados(repo)` CONTANDO POR MES y sin imprimir sus claves, que llevan la fecha del caso | se pregunta |
| Lo que difiere A PROPOSITO | el encargo o la respuesta a la PARADA | si no se dice, todo tiene que salir identico |

## Limites

- **Dos clones desechables, desacoplados de toda rama**, fuera del repo, en un directorio temporal
  de RUTA CORTA (una carpeta de un solo nivel en la raiz del disco, p. ej. `C:\cm`):
  `git worktree add --detach <tmp>/main main` y `git worktree add --detach <tmp>/rama HEAD`, con la
  rama ya commiteada. Nunca `--force` (dejaria dos worktrees sobre la misma rama) y nunca un
  `git checkout` de otra cosa en el repo real. Por que la ruta corta: con el clon en la carpeta
  temporal de la sesion, `tests/unit/test_rutas_windows.py`
  (`test_las_rutas_por_defecto_con_el_rotulo_mas_largo_caben_en_este_repo`) fallo por pasar del
  limite de 259 caracteres de Windows (263), y un fallo que solo existe en el clon no es una
  regresion (respuesta del consultor del 2026-10-11 en `trabajo/entorno-code`, punto 5).
- **Las velas no se copian ni se descargan.** Cada clon lleva su `config/settings.local.toml`
  (ignorado por git) con `[entorno] nombre = "backtest"` y `[rutas] corpus = "corpus"`,
  `knowledge = "knowledge"` y `data = "<ruta absoluta del data/ real>"`: las tres claves de
  `[rutas]` son obligatorias (`src/botsito/config/ajustes.py`). Antes de ejecutar nada se comprueba
  LEYENDO EL CODIGO que los comandos no escriben en `data/` (fichero:linea); si escriben, se para.
- **El universo se acota con las opciones de los propios comandos**, nunca borrando manifiestos: un
  manifiesto que falta hace fallar `kit check` («datasets congelados que ya no estan en
  data/manifests», `src/botsito/cases/paquete.py`) y la comparacion deja de medir lo que dice. Si un
  comando no tiene opcion para acotar y leeria dias reservados, se para y se dice.
- **Una comparacion que falla igual en los dos lados no es una regresion superada**: si un comando
  sale con error en main y en la rama, se dice y no cuenta como «identico».
- **Holdout**: lo que lean `kit build` y `kit check` de dias reservados lo declaran ellos por
  recuento, y se copia al informe. No se lista `data/` ni ninguna carpeta con meses reservados.
- **El arnes** (`uv run botsito motor arnes`) solo se ejecuta si el encargo o la respuesta a la
  PARADA lo autorizan expresamente; en la duda, PARADA.
- Nada de lo hecho en los clones (sesiones sinteticas, ficheros generados) se commitea, y ningun
  tag ni rama se crea en ellos.

## El recorrido

1. Antes: `git status --short`, `git branch --list` y `git tag -l` del repo real, anotados.
2. Crear los dos worktrees y su `config/settings.local.toml`.
3. Comprobar en el codigo que los comandos no escriben en `data/`.
4. Ejecutar los MISMOS comandos, con los mismos argumentos, en los dos clones, cada uno con su
   salida a ficheros dentro de su clon, y anotar el codigo de salida de cada comando.
5. Comparar: `sha256sum` de cada fichero de salida en los dos lados, en una tabla
   `fichero · hash main · hash rama · igual`. Lo que difiera: `diff` recortado al cambio, y la
   comprobacion de que es EXACTAMENTE lo declarado y nada mas.
6. `git worktree remove <tmp>/main` y `<tmp>/rama` (con `--force` solo si quedan ficheros generados
   sin seguir, y diciendolo), `git worktree prune`. Despues, `git status --short`,
   `git branch --list`, `git tag -l` y `git ls-remote --heads --tags origin` comparados con el
   paso 1: nada nuevo ni en local ni en origin.

## Para probar un test «con el codigo de main»

Mismo mecanismo: el clon `--detach` de `main`, el test de la rama copiado DENTRO de ese clon,
ejecutado alli, y la salida (que debe fallar) pegada al informe. Nunca se cambia de rama en el repo
real para esto.

## Artefacto

En el informe, «Regresion contra main»: los comandos tal cual y su codigo de salida en cada lado, el
universo y su comprobacion, los dias reservados leidos por recuento, la tabla de hashes, los diff de
lo que difiere a proposito, y el estado del repo real (y de origin) antes y despues.

## Verificacion

- `git worktree list` sin los clones al terminar.
- La tabla de hashes cubre todo fichero de salida de los dos lados, ni uno de mas ni de menos.
- Ningun comando salio con error en los dos lados sin decirlo.
- Lo que difiere es solo lo declarado.
