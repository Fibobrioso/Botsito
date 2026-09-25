# La entrada de marzo

Como entra el backtest de MARZO de 2026 por el camino de fidelidad, en el orden de ADR-0046 §6.
Escrito el 2026-09-24 en la rama `trabajo/entrada-marzo`, cuando todavia NO hay material de marzo:
ni libro, ni tramo, ni reparto. Cada paso trae el comando tal como se invoca, lo que tiene que
salir y **donde para la sesion**.

El orden entero esta ensayado sobre un repo sintetico con la CLI real:
`tests/contract/test_ensayo_marzo.py`. Antes de empezar, en la rama de la entrada:

```
uv run pytest tests/contract/test_ensayo_marzo.py -q
```

Tiene que salir `1 passed`. Si no, no se empieza.

## Lo que no cambia en ningun paso

- **La sesion NO abre el libro de marzo antes del paso c**, y en el c solo lo abre la herramienta
  del huso, con las filas de los dias `fidelidad-dev`. La columna de fechas del paso a la lee Aleks,
  no la sesion (ADR-0046 §6a, excepcion acotada a ADR-0039 §1).
- **EL SORTEO NO SE REPITE NUNCA** (ADR-0046 §5): ni con otra semilla, ni borrando la carpeta, ni
  despues de un huso NO CONCLUYENTE. `fidelidad build` se niega solo, y nadie lo rodea.
- **Toda lectura se declara el mismo dia** en `docs/validation/HOLDOUT-EXPOSICIONES.md` (ADR-0021 §4).
- **Todo commit que toque `knowledge/cases/` lleva `Fuente:`** en el cuerpo, con ids que existan.
- **Cada commit, en este orden: estadiar lo que entra → `make check > make-check.log 2>&1` →
  commit** (2026-09-25, `trabajo/blindaje`). `make check` en verde sella el arbol estadiado y el
  hook rechaza un commit sin ese sello. La salida, a un fichero y nunca a `/dev/null`.

## Paso 0 · La entrega, y la primera parada

Lo de la entrega esta en `PROJECT_STATE.md`, Next Action 2 y 12: el xlsx al corpus, marzo en
`vistos.yaml` y la confirmacion del trader por escrito. Aqui solo lo que el orden necesita:

```
uv run botsito corpus inventory
git diff --stat knowledge/corpus/manifest.yaml
```

El diff tiene que traer SOLO la entrada nueva del libro de marzo, con su `ruta` y su `sha256`. En
lo que sigue, `<LIBRO>` es `corpus/Estrategia del trader/<ruta>` y `<SHA>` es su `sha256`.

> **PARADA 0.** Sin el xlsx de marzo en el corpus no se empieza. La sesion no busca el fichero
> fuera del corpus ni lo pide por otra via.

## Paso a · Las fechas, las lee Aleks: segunda parada

> **PARADA A. La sesion para aqui y no abre el libro.** Aleks abre SOLO la columna de fechas, UNA
> vez, antes del sorteo, y entrega tres cosas:
>
> 1. **El tramo**: la INTERSECCION de los dias que salen leyendo `dateStart` con UTC y con
>    Europe/Madrid -`desde` el mayor de los dos primeros dias, `hasta` el menor de los dos
>    ultimos-. Un dia dudoso de borde no entra.
> 2. **El formato** de `dateStart`, que tiene que ser del vocabulario de `corpus.libros.FORMATOS`:
>    `AAAA/MM/DD HH:MM:SS` o `AAAA-MM-DD HH:MM:SS`. Si es otro, se para: un formato nuevo entra en
>    el vocabulario solo con su medida (ADR-0039 §2).
> 3. **Su fila en `HOLDOUT-EXPOSICIONES.md`**, ese mismo dia. Declara el rango, no la lista de dias.
>
> **PARADA A2. Si la columna trae fechas con MAS DE UN formato**, no se elige uno ni se sigue: en el
> paso c el lector parsea cada fecha solo con el formato dado, y una que no case para la medida
> entera, porque de esa fila no se sabe de que dia es. **No se toca el lector sobre la marcha.** Se describe el
> caso -cuantas filas en cada patron y cual es el patron (p. ej. `AAAA-MM-DD HH:MM:SS`), SIN
> mostrar ninguna fecha, porque puede ser de un dia que el sorteo reserve- y se espera al
> consultor (decision del 2026-09-24).

Con eso, la sesion anade el tramo SIN `material_sha256` -todavia no hay libro declarado- a
`knowledge/cases/fidelidad/config.yaml`:

```yaml
cobertura_material:
  "2026-03":
    - desde: "2026-03-DD"
      hasta: "2026-03-DD"
      entregado_el: "AAAA-MM-DD"
      fuente: [<commit de la entrega>, ADR-0046]
```

```
uv run botsito knowledge validate > knowledge-validate.log 2>&1
```

Tiene que salir sin `ERROR`; `knowledge-validate.log` se borra y no se commitea. Commit con
`Fuente: ADR-0046`.

## Paso b · El sorteo

> **PARADA B0 (2026-09-25, rama `trabajo/sesion-02`). Si A-42 no esta RESUELTA, marzo se detiene
> aqui, tras el paso a.** A-42 pregunta con que reloj cuenta el trader su horario de 07:00 a
> 15:00. El grafico de FX Replay es UTC+2 fijo, `huso_operativa` sigue en Europe/Madrid, y en
> invierno las dos lecturas se separan una hora. En 2026 el horario de verano europeo empieza el
> 29 de marzo, asi que casi todo marzo es invierno. **Por que aqui y no antes de la ingesta:**
> este paso congela `huso_operativa` en `ventanas.yaml`, junto con la ventana de cada caso, y el
> sorteo no se repite (ADR-0046 §5). Parar despues ya no arreglaria nada. Antes del comando, el
> estado se mira en `knowledge/spec/ambiguedades.yaml` (entrada `A-42`, campo `estado`). Si no dice
> `RESUELTA`, la sesion para aqui y lo informa, y los pasos b a e no se ejecutan.

La semilla la fija el consultor ANTES de ejecutarlo: por el precedente de septiembre es
`AAAAMMDD`, la fecha en que se fija el reparto (`SEPTIEMBRE-SORTEO.md` §4), y va en el mensaje
del commit.

```
uv run botsito fidelidad build --artefacto eurusd-2026-03 --seed <SEMILLA>
```

Tiene que salir:

- lineas `LECTURA:` con los datasets y CUANTOS dias reservados se leen por particion, sin fechas;
- `OK: knowledge/cases/fidelidad/eurusd-2026-03: N casos de un universo de N (+ X dias
  excluidos), seed <SEMILLA>. ANCLALO en este mismo commit: [...]`. **Los dos N tienen que ser
  iguales**: la regla de `cupos_por_mes` reparte el universo entero.

En `knowledge/cases/fidelidad/eurusd-2026-03/particiones.yaml`, `cupos` tiene que ser la regla
aplicada a N: `fidelidad-dev` = ⌊N/3⌋, `fidelidad-2` = ⌊(N − dev)/2⌋, `fidelidad-3` el resto y
`fidelidad-1` = 0. Y todos los casos son `caso-eurusd-2026-03-*`.

```
uv run botsito fidelidad anclar --artefacto eurusd-2026-03
uv run botsito fidelidad check --artefacto eurusd-2026-03
```

Tienen que salir `OK: eurusd-2026-03 anclado en knowledge/cases/fidelidad/anclas.yaml: [...]` y
`OK: eurusd-2026-03 se recompone igual desde el repo y data/`. El artefacto y su ancla van en el
MISMO commit, con `Fuente: ADR-0046` y la semilla en el mensaje.

> **PARADA B.** Si `fidelidad build` falla ANTES de escribir la carpeta, no se ha sorteado nada:
> se informa y se para. Si falla DESPUES, o si algo del reparto parece mal, **no se vuelve a
> sortear**: se informa y decide el consultor. `fidelidad build` ya se niega a repetir un id con
> carpeta, ancla o historial.

## Paso c · El huso, por velas, con la herramienta

Primero el CONTROL, sobre ABRIL -nunca mayo-, con la herramienta tal como esta commiteada:

```
uv run python scripts/huso_por_velas.py --libro "corpus/Estrategia del trader/Material adicional de su operativa/backtesting-analytics ABRIL 2026.xlsx" --mes 2026-04 --salida control-abril.txt
diff control-abril.txt docs/validation/HUSO-POR-VELAS-CONTROL-ABRIL.txt
rm control-abril.txt
```

La herramienta sale con `0` y el `diff` sale vacio: UTC 36/38, Europe/Madrid 4/38,
`== VEREDICTO (ADR-0039 §5): UTC` y `== CONTROL: declarado UTC -> COINCIDE`.

> **PARADA C1.** Si la herramienta sale con `3` (NO COINCIDE) o el `diff` no esta vacio, el metodo
> no sirve hoy: se para y se informa. **No se toca la herramienta ni `criterio_huso.yaml` para que
> cuadre.**

Despues, marzo, con el formato que dio Aleks en el paso a:

```
uv run python scripts/huso_por_velas.py --libro "<LIBRO>" --mes 2026-03 --formato "<FORMATO>" --salida docs/validation/HUSO-MARZO.txt
```

Tiene que salir, sin fechas ni precios:

```
LIBRO: <sha 12>... formato '<FORMATO>'
CRITERIO: knowledge/corpus/criterio_huso.yaml (margen 2 puntos; decide >= 0.90 y el otro <= 0.50)
DATASETS: eurusd-m1-2026-03-989392e8
DIAS dev: <⌊N/3⌋>
FILAS comparables: <n>; sin entrada numerica: <k>; descartadas por frontera de dia: <si|no>
UTC: <d>/<n> = <x> %
Europe/Madrid: <d>/<n> = <x> %
== VEREDICTO (ADR-0039 §5): <UTC | Europe/Madrid | NO CONCLUYENTE>
```

Se declara en `HOLDOUT-EXPOSICIONES.md`: de las filas de los dias `fidelidad-dev`, `dateStart` y
`entryPrice`, dos lecturas, una por huso. De las filas reservadas, `dateStart` se parsea en memoria
para saber de que dia son -el lector lo hace por construccion- y no sale nada.

> **PARADA C2. Si la herramienta sale con `ERROR: [...] una fila tiene dateStart que no casa con
> ningun formato declarado para este libro`**, hay fechas con un formato distinto del del paso a,
> y la medida entera se para: es lo correcto, no un fallo que rodear. **No se toca el lector ni la
> herramienta sobre la marcha, y no se prueba otro `--formato`** hasta que uno parsee (ADR-0039
> §1). La sesion describe el caso -cuantas filas y que patron, SIN mostrar ninguna fecha: pueden
> ser de dias reservados- y espera al consultor (decision del 2026-09-24).

> **PARADA C3. Si el veredicto es NO CONCLUYENTE, la rama para aqui** (ADR-0046 §5): el libro NO se
> declara, los dias reservados siguen reservados, los `fidelidad-dev` esperan una decision del
> consultor, y el sorteo NO se repite.

## Paso d · La declaracion del libro

Se anade la entrada a `knowledge/corpus/libros.yaml` -SOLO ANADIR: una entrada commiteada no se
edita ni se borra nunca (ADR-0039 §3)- y, en el MISMO commit, `material_sha256: <SHA>` al tramo
de marzo de `knowledge/cases/fidelidad/config.yaml`:

```yaml
  "<SHA>":
    fichero: "<ruta>"
    lecturas:
      - formato: "<FORMATO>"
        huso: <VEREDICTO>
    medida: >-
      Velas, AAAA-MM-DD (scripts/huso_por_velas.py, docs/validation/HUSO-MARZO.txt), SOLO sobre
      filas de los dias fidelidad-dev cuyo dia sale igual con los dos husos: UTC <d> de <n>,
      Europe/Madrid <d> de <n>. Control con el mismo metodo y umbral: abril (36/38 frente a 4/38).
    declarado_el: "AAAA-MM-DD"
    fuente: [ADR-0039, ADR-0046]
```

> **PARADA D. La sesion escribe la entrada y PARA antes del commit.** Es la unica escritura de la
> entrada que no se puede deshacer: si la entrada esta mal, el libro deja de leerse hasta que otro
> ADR decida. El commit lo autoriza el consultor despues de leerla.

```
uv run botsito knowledge validate > knowledge-validate.log 2>&1
uv run python scripts/huso_por_velas.py --libro "<LIBRO>" --mes 2026-03 --salida control-marzo.txt
rm control-marzo.txt knowledge-validate.log
```

`knowledge validate` tiene que dar `OK: <n> libros declarados con formato y huso, solo-anadir
intacto, cruzados con cobertura_material`, uno mas que antes, y un `AVISO` esperado:
`eurusd-2026-03/ventanas.yaml: su config congelado difiere del config.yaml de hoy en
cobertura_material`, porque el sha se anade despues del sorteo y el artefacto se reproduce con lo
que congelo. La herramienta, ya como control del
libro recien declarado, sale con `0` y `== CONTROL: declarado <VEREDICTO> -> COINCIDE`. Commit con
`Fuente: ADR-0039, ADR-0046`.

## Paso e · La ingesta de los `fidelidad-dev`

```
uv run botsito casos ingerir --material "<LIBRO>" --fecha AAAA-MM-DD --artefacto eurusd-2026-03
```

Tiene que salir por stdout:

```
INGESTA: <K> casos escritos de <⌊N/3⌋> dias ingeribles; <F> filas leidas; 0 pestanas de agregado abiertas
OK: knowledge/cases/dev/ con <K> casos. Commitealos con `Fuente:`
```

Por stderr pueden salir, CONTADOS y nunca nombrados, las filas sin `initialSL` y los dias
ingeribles sin ninguna operacion: se copian al informe tal cual.

```
uv run botsito casos check
```

`casos check` da `OK: los casos de la biblioteca tienen la forma declarada y ninguno esta
reservado`. Se declara la lectura en `HOLDOUT-EXPOSICIONES.md` -`dateStart`, `side`, `entryPrice` e
`initialSL` de las filas de los dias `fidelidad-dev`- y, con todo escrito, se estadia, se prueba y
se commitea, en ese orden:

```
git add knowledge/cases/dev/ docs/validation/HOLDOUT-EXPOSICIONES.md
make check > make-check.log 2>&1
grep "SELLO: make check en verde" make-check.log
rm make-check.log
```

`make check` sale con 0 y el `grep` da una linea: entonces se commitea con `Fuente: ADR-0046`.

> **PARADA E.** Cualquier `ERROR` de la ingesta: no se escribe nada, se informa y se para. No se
> prueba con otro libro ni con otro artefacto.

## Y aqui acaba

Informe de la rama en `docs/validation/`, estado WAITING_FOR_USER_VALIDATION, y el ritual de
cierre lo ejecuta el usuario (`docs/runbooks/RITUAL.md`). Con esto **no se mide la fidelidad de
nada**: la parte `fidelidad-dev` de marzo pasa a ser conjunto de medida de desarrollo junto con
mayo (ADR-0043, aclarado por ADR-0046 §2), y lo que caiga en `fidelidad-2` y `fidelidad-3` queda
oculto detras de la puerta de ADR-0033.
