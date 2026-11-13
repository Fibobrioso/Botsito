# GUARDIA-FALSOS-POSITIVOS · un literal «// » y cmp, sin abrir ningun hueco

Rama `trabajo/guardia-falsos-positivos` (carril «guardias y deuda»: G.6 de la hoja de ruta y la
deuda de la guardia que dejo `trabajo/capa-generada`). Encargo del consultor del 2026-11-12:
`docs/encargos/trabajo-guardia-falsos-positivos.md`.

## Apertura (2026-11-12)

Base comprobada con git y gh antes de abrir:

- `git rev-parse main origin/main`: `4ecd7f17e89cc5e4bd8b999435bdf104b5e23e32` las dos veces
  (`git rev-parse --short main` = `4ecd7f17`, el commit de estado de `stable/F38z-capa-generada`).
- `git rev-parse "stable/F38z-capa-generada^{commit}"` = `git rev-parse main^1` =
  `7bccf3103250f6d89e0877e993cda2e449a3423f`; el tag esta en origin (`git ls-remote --tags`:
  `fde7d35a… refs/tags/stable/F38z-capa-generada`). `trabajo/capa-generada` esta cerrada: su
  registro de cierre es el ultimo de `docs/state/HISTORIA.md` y `git ls-remote --heads origin` solo
  da `main`.
- CI de `main` sobre `4ecd7f17…` (check-runs, con `gh api`): `python completed success`, check-run
  131643256110. El clasificador no nego `gh`.
- `git branch --list`: solo `main`; `git ls-remote --heads origin "fix/*"`: vacio.
- `PROJECT_STATE.md`: 24.380 bytes en main; 24.569 tras la apertura (tope 25.000 de
  `tests/unit/test_project_state.py`). El cierre tendra que recortar antes de anadir.

Exposicion: cada `make check` lee el M1 entero de marzo y calienta con el de junio (Technical
Debt); la fila del 2026-11-12 de esta rama en `docs/validation/HOLDOUT-EXPOSICIONES.md` se escribio
antes del primero.

Negativa de la guardia durante la apertura (no del objeto de la rama): un comando mio de solo
lectura con una variable de shell (`c=$(git log ...)`) lo nego `NOMBRES_DE_ENTORNO`; se reescribio
como la propia guardia propone («sin esa variable»), en dos llamadas.

Otras dos negativas de la guardia a comandos mios de la apertura y la fase 0, las dos con la forma
que ella propone: `git add ...; uv run python scripts/contrato_rama.py` en una llamada (una ejecucion
detras de otra orden: partido en dos llamadas) y `git ls-files | grep ...` desde la raiz (ADR-0088:
lo busque con Glob y rutas literales). Ninguna es del objeto de la rama.

## Fase 0 (2026-11-12)

Sin tocar `guardia.py`. Lo que escribe la fase 0, declarado:

- `tests/unit/test_guardia_falsos_positivos.py`, **un test de medida** (`test_fase0_tabla`) que no
  asegura nada de F1 ni de F2: imprime, por caso, la decision de la guardia de hoy y la de cuatro
  variantes de D1 SIMULADAS con `monkeypatch` (sin cambiar `guardia.py`), con D2 tambien simulado
  (`cmp` en `NO_EJECUTAN`), y el tiempo de cada `decidir()`. Va en `tests/` porque la guardia niega
  ejecutar suelto un guion que monta rutas protegidas a trozos (la cabecera de `medir_g1.py`); tras
  la respuesta, el fichero pasa a tener los tests de la rama.
- `anexos/GUARDIA-FALSOS-POSITIVOS/fase0-windows-SALIDA.txt`: su salida en Windows (232 lineas;
  rutas protegidas como `<holdout>`, el temporal como `<tmp>`, el nombre del equipo como
  `<equipo>`). Corrida con `--basetemp=C:/gfp-fase0`: el temporal de pytest en Windows lleva
  `AppData\`, que casa con el fragmento `data\` de `SENSIBLES` y contaminaba dos casos (h7 y h8)
  en una primera corrida; la raiz del repo real no lleva ningun fragmento.
- `anexos/GUARDIA-FALSOS-POSITIVOS/medir_windows.py`: como resuelve Windows de verdad las rutas que
  empiezan por dos barras y un blanco (apunta solo a `C:\Windows\win.ini`). **La guardia nego
  ejecutarlo** («la ruta `// x/../C:/Windows/win.ini` no se puede canonizar»): es la conducta que
  esta rama no debe cambiar. No lo reescribi: PARADA, y si hace falta lo lanza Aleks con «!»
  (decision 3). *(Tras la respuesta, punto 3: no se lanza y sale del repo; estuvo en `dce4004e`.)*

### a. F1 y F2 reproducidos

Repo sintetico de `tmp_path` con ficheros falsos; cada guion es NUEVO en la rama (no esta en el
`main` sintetico). Columnas: `hoy` es la guardia del arbol (igual a la de `stable/F38z`); las demas,
con la variante de D1 simulada Y con D2 (cmp en `NO_EJECUTAN`). Variantes de D1:

- **D1**, tal cual el encargo: un literal cuyos dos primeros caracteres son separadores seguidos de
  un espacio o un tabulador no llega a `_absoluta`.
- **D1a**: D1, salvo que el literal lleve un fragmento de `SENSIBLES` (guardia.py:4244-4256): ese
  se sigue mirando como ruta.
- **D1b**: D1a, y ademas salvo que el codigo recorra (`CODIGO_QUE_RECORRE`).
- **D1c**: D1, salvo que el tramo hasta el siguiente separador, sin los blancos del principio, NO
  lleve un blanco. Un nombre de maquina no lleva blancos, asi que ese tramo no puede ser una
  maquina. Es un hecho negativo, no una gramatica de «nombre de maquina».
- **D1d**: D1a y D1c a la vez.

| caso | grupo | hoy | D1+D2 | D1a+D2 | D1b+D2 | D1c+D2 | D1d+D2 |
|---|---|---|---|---|---|---|---|
| f1-copia-generar-capa | F1 | niega | pasa | pasa | pasa | pasa | pasa |
| f1-literal-364 | F1 | niega | pasa | pasa | pasa | pasa | pasa |
| f1-literal-359-fcadena | F1 | niega | niega | niega | niega | niega | niega |
| f1-tabulador | F1 | niega | pasa | pasa | pasa | pasa | pasa |
| f1-barras-invertidas | F1 | niega | pasa | pasa | pasa | pasa | pasa |
| f1-mql5-pipe | F1 | pasa | pasa | pasa | pasa | pasa | pasa |
| f1-mql5-pipe-con-barras | F1 | niega | niega | niega | niega | niega | niega |
| f1-mql5-mas | F1 | pasa | pasa | pasa | pasa | pasa | pasa |
| d3-host-share-barras | D3 | niega | niega | niega | niega | niega | niega |
| d3-host-share-invertidas | D3 | niega | niega | niega | niega | niega | niega |
| d3-recorre-protegida | D3 | niega | niega | niega | niega | niega | niega |
| d3-nombra-protegido | D3 | niega | niega | niega | niega | niega | niega |
| h1-recorte | hueco | niega | **pasa** | niega | niega | niega | niega |
| h1b-recorte-control | hueco | pasa | pasa | pasa | pasa | pasa | pasa |
| h1c-recorte-blanco-interior | hueco | niega | **pasa** | niega | niega | **pasa** | niega |
| h2-lstrip | hueco | niega | **pasa** | niega | niega | niega | niega |
| h3-puntopunto | hueco | niega | **pasa** | niega | niega | niega | niega |
| h4-espacio-localhost | hueco | niega | **pasa** | niega | niega | niega | niega |
| h5-tab-localhost | hueco | niega | **pasa** | niega | niega | niega | niega |
| h6-espacio-equipo | hueco | niega | **pasa** | niega | niega | niega | niega |
| h7-espacio-localhost-raiz-recorre | hueco | niega | **pasa** | **pasa** | niega | niega | niega |
| h8-espacio-localhost-raiz-sin-recorrer | hueco | niega | **pasa** | **pasa** | **pasa** | niega | niega |
| f2-cmp-docs-nuevos | F2 | niega | pasa | pasa | pasa | pasa | pasa |
| f2-cmp-s-docs-nuevos | F2 | niega | pasa | pasa | pasa | pasa | pasa |
| f2-cmp-docs-de-main | F2 | pasa | pasa | pasa | pasa | pasa | pasa |
| f2-cmp-origen-g6 | F2 | niega | pasa | pasa | pasa | pasa | pasa |
| f2-cmp-protegido-segundo | F2 | niega | niega | niega | niega | niega | niega |
| f2-cmp-protegido-primero | F2 | niega | niega | niega | niega | niega | niega |
| f2-cmp-protegido-absoluto | F2 | niega | niega | niega | niega | niega | niega |
| c-diff-docs-nuevos | diff | pasa | pasa | pasa | pasa | pasa | pasa |
| c-diff-q-docs-nuevos | diff | pasa | pasa | pasa | pasa | pasa | pasa |
| c-diff-protegido | diff | niega | niega | niega | niega | niega | niega |
| c-diff-protegido-primero | diff | niega | niega | niega | niega | niega | niega |

**F1** (Windows): «la ruta `// CAPA_HASH = SHA-256 de este fichero sin su linea
(docs/validation/CAPA-GENERADA.md).` no se puede canonizar (un recurso de otra maquina...)». Lo
lanza `_no_canonizable` (guardia.py:1330-1336), llamada desde `_sin_prefijos` (:1362): su regex de
recurso de red (:1356) casa con equipo «` CAPA_HASH = ... (docs`» y recurso «`validation`», que no
es la propia maquina. Llega por `analizar_codigo` (:4947, `_absoluta`) → `_absoluta` (:1309) →
`_canonica` (:1371-1372, solo si `os.name == "nt"`). La copia cambiada de `generar_capa.py` se
niega por el literal de :364 (`ast.walk` lo encuentra antes). **Hay un segundo literal de F1 en el
mismo fichero, oculto detras: :359**, el trozo constante de la f-cadena
(«`//   uv run python src/botsito/mql5bridge/generar_capa.py --repo . --perfil `»), con tres
espacios. Lo cubren D1 y sus variantes (lleva blanco tras `//`); con todas, la copia del guion
real pasa.

En **Linux** F1 no existe: `_canonica` no llama a `_sin_prefijos`, y `realpath` deja la ruta en
`/ CAPA_HASH...`, fuera de la raiz (codigo, :1371; lo medira la CI de `fix/`, donde
`test_fase0_tabla` corre e imprime). Los casos h4-h8 llevan `\`, que en Linux es parte del nombre.

**F2** (Linux y Windows): «ejecutar `cmp`: la guardia no sabe con que se ejecuta docs/n1.md (ni
extension ni `#!`).». `cmp` no esta en `NO_EJECUTAN` (:2836-2892), cae en
`_ejecucion_de_un_programa_desconocido` (:1794-1795, :3528), y `_ficheros_de_un_programa_desconocido`
(:3505-3525) toma cada argumento que es un fichero que existe. Matiz del auditor: solo se niega si
el fichero no es el de `main`; `cmp docs/a.md docs/b.md` con los dos en `main` pasa hoy (fila
`f2-cmp-docs-de-main`). Por eso D4 («cmp sobre dos ficheros de docs/») se mide con dos ficheros
NUEVOS de `docs/` del repo sintetico, y con el nombre del origen de G.6
(`diaria.DIAGNOSTICO.cuenta=diaria.txt`, ACTIVAR-SESION-06-MOTOR.md:217-218, que el auditor
encontro: de capa-generada no quedo la orden literal, del origen de G.6 si).

**Tiempo (D6)**: ningun caso pasa de 0,13 s en `decidir()`. Con D1 y sus variantes el literal de
F1 no llega a `_absoluta` ni a `realpath`; hoy tampoco: `_no_canonizable` lanza antes de
`realpath` (:1372 frente a :1376).

### b. Los casos de D3 con la guardia de hoy

- Los de `test_guardia_alias.py` y `test_guardia_g1.py`: siguen en la suite; hoy pasan (es decir,
  niegan) en el `make check` de la apertura (3465 passed). Matices del auditor: :183-199 son alias
  de la PROPIA raiz (`\\?\`, `//?/`, UNC a localhost o al equipo, 8.3, punto final) que se niegan
  por la regla del sitio, no por canonizar (test :224-237); :439-463 si son los no canonizables
  (otra maquina, `\\.\pipe`, GLOBALROOT, Volume, UNC), con `SOLO_WINDOWS`; :512-520 es `_dobladas`;
  `file://` es :623-631 (el `skipif` en :622). **Ninguno pasa por `analizar_codigo`**: van por
  Read, Grep y `cat` (:456-460), es decir por `_absoluta` directa, que D1 no toca.
- Los de esta rama, en la tabla: `//host/share/...` y `\\host\share\...` en un guion nuevo
  (niegan, en Windows; en Linux pasan hoy, son nombres raros fuera de la raiz: sus tests seran de
  solo Windows), cmp con un fichero protegido (niega hoy por «ejecutar <holdout>/...», y con D2 por
  «leer el contenido de <holdout>/...»: el test mirara la regla, `R_HOLDOUT`, no el texto), y un
  guion nuevo que nombra y recorre una carpeta protegida (niega).
- **D1 tal cual deja pasar ocho casos que hoy se niegan** (h1-h8): un literal de D1 con la ruta
  protegida que el codigo recorta al ejecutarse (`[3:]`, `.lstrip('/ ')`), un `// x/../<raiz>/...`
  y la raiz como recurso de la propia maquina con un blanco delante del nombre (`\\ localhost\C$\`,
  con tabulador, con el nombre del equipo). Contradice D3 («ningun caso que hoy se niega deja de
  negarse»): PARADA (decision 0). Si h3-h8 abren algo de verdad en Windows depende de como resuelve
  Windows un servidor con un blanco delante: es lo que mide `medir_windows.py`, que la guardia nego
  (decision 3). h1 y h2 abren seguro: el codigo recorta antes de `open`.
- **h1b ya pasa hoy y pasa con todas las variantes**: `'x' + <ruta protegida>` recortado con `[1:]`.
  La guardia no sigue lo que el codigo hace con un literal al ejecutarse; ninguna variante de D1 lo
  cambia ni lo empeora. No es de esta rama; queda declarado (decision 4).

### c. diff y G.6

`diff` esta en `NO_EJECUTAN` (guardia.py:2857, «compara ficheros»); sus argumentos van a
`_exigir_args_legibles` (:1820-1833). Medido: `diff` y `diff -q` de dos ficheros nuevos de `docs/`
pasan; con un fichero protegido, primero o segundo, niega («leer el contenido de ...»). Solo `cmp`
se negaba (en el origen de G.6, ACTIVAR-SESION-06-MOTOR.md:217-221, solo se nego `cmp`; `diff`
entro en el titulo de G.6 por la propuesta). **G.6 se cierra con F2.**

### d. El cambio que propongo, y los tests que rompen con la guardia de stable/F38z

**D1** (la variante de la decision 0; recomiendo D1d, y solo en Windows): en `analizar_codigo`,
dentro del bucle de literales (guardia.py:4939-4962), entre el `file:` (:4944-4946) y
`ruta = _absoluta(lit, ctx.cwd)` (:4947):

```python
if _no_es_ruta(lit):  # F1 (trabajo/guardia-falsos-positivos)
    continue
```

con `_no_es_ruta` junto a `_literales` (:4980), con su porque y su origen en un comentario:
`os.name == "nt"`, `re.match(r"[\\/]{2}[ \t]", lit)`, el tramo hasta el siguiente separador
(sin los blancos del principio) lleva un blanco, y ningun fragmento de `SENSIBLES` en
`lit.lower()`. Ni `_sin_prefijos`, ni `_canonica`, ni `_absoluta` cambian: Read, Grep y Bash siguen
igual. Solo en Windows porque F1 solo nace ahi (en Linux el literal ya pasa por `realpath`, y saltar
el literal en Linux seria cambiar algo que no falla).

**D2**: `"cmp"` en `NO_EJECUTAN`, al final, en un bloque de esta rama (tras :2891): «compara dos
ficheros byte a byte; no ejecuta ninguno (G.6; sus argumentos se miran como una lectura, como los de
`diff`)». No hace falta mas: el programa en `NO_EJECUTAN` ya cae en `_exigir_args_legibles`
(:1820-1833), medido en las filas `f2-cmp-protegido-*` con D2.

**Tests** (en `test_guardia_falsos_positivos.py`, que sustituye al test de medida), y cuales FALLAN
con la guardia de `stable/F38z` (que es la de hoy):

| test | con stable/F38z | con la rama | sistema |
|---|---|---|---|
| la copia cambiada de `generar_capa.py` pasa (F1, :364 y :359) | falla (niega) | pasa | solo Windows |
| un literal `// `, `//\t` y `\\ ` de un guion nuevo pasa | falla | pasa | solo Windows |
| `cmp` y `cmp -s` de dos ficheros nuevos de `docs/`, y el nombre con `=` de G.6, pasan | falla | pasa | los dos |
| cmp con un fichero protegido (primero, segundo, absoluto) niega con `R_HOLDOUT` | pasa | pasa | los dos |
| h1-h8 siguen negados | pasa | pasa | h1-h8 Windows; h3 tambien en Linux |
| `//host/share/...` y `\\host\share\...` de un guion nuevo siguen negados | pasa | pasa | solo Windows |
| un guion nuevo que nombra y recorre una carpeta protegida sigue negado | pasa | pasa | los dos |
| ROTO A PROPOSITO: sin la clausula de `SENSIBLES`, h1/h2/h3/h1c pasan; sin la del blanco, h4-h8 pasan; sin el `os.name`, nada cambia en Windows (se dice); sin `cmp` en `NO_EJECUTAN`, F2 se niega; con `cmp` sin leer sus argumentos, el protegido pasa | — | cada test sostenido falla | lo de F1, Windows |

**D5** (la referencia), con dos matices del auditor que lo hacen posible: `GUARDIA_DE_REFERENCIA`
pasa a `stable/F38z-capa-generada` (test_guardia_g1.py:914) y `CAMBIOS_DECLARADOS` (medir_g1.py:59-84)
se vacia; pero (1) F1 y F2 **no son casos de `medir_g1.py`** (ninguno lleva `cmp` ni un literal con
`//`): se anaden a su lista de casos y a su `preparar()`, y solo entonces se declaran; F1 solo
difiere en Windows y F2 en los dos; (2) `test_roto_la_comparacion_con_main` (:1021-1030) borra la
clave `a1-lector-rama`, que ya no estara: pasa a borrar la de F2 (la que difiere tambien en la CI de
Linux). Y (3) el orden: subir la referencia antes de cambiar `guardia.py` rompe
`test_la_referencia_es_un_tag_y_no_es_esta_guardia` (:943-949, exige guardias distintas, y hoy la
del arbol es la de F38z): va en el mismo commit que el cambio de la guardia.

### e. Herencias

| Donde | Que dice | Entra / por que no |
|---|---|---|
| PROJECT_STATE.md:84 (Technical Debt, entro con F38z) | `//` como ruta, `cmp a b` como ejecutar `a`, `compilar.py` por `/` | Entra: F1 y F2 se resuelven; la linea se reescribe en el cierre (§7 del informe final) |
| PROJECT_STATE.md:152 (Technical Debt) | « / » entre espacios, `</li>` y `$'\r'` | No entra (punto 2 del encargo). **Dos correcciones del auditor al encargo**: entro con F38w (`trabajo/laminas`, `git blame` 6871ac96), no con F38y; y `$'\r'` NO es el mismo mecanismo: es `tokenizar` (:934-946, la comilla ANSI-C con barra da valor desconocido), no los literales de `analizar_codigo`. La linea del cierre lo dira asi |
| HOJA-DE-RUTA.md:792-798 (G.6) | cmp y diff de dos ficheros que no son guiones | Entra: se cierra con F2 (c) |
| HOJA-DE-RUTA.md:712-721 (G.1) | los candidatos en blanco tras `:` y `@` de `candidatos_de_ruta` (§4.5), y lo de cerrar-rama | No entra: el encargo solo excluye D; G.1 no es de este encargo y toca `.claude/skills/` (protegido) |
| PROJECT_STATE.md:110 (Technical Debt) | otro falso positivo: ffmpeg `-ss`/`-t` sobre un tramo del corpus | No entra: otra regla (la lista cerrada de ffmpeg); no la pide el encargo |
| GUION-MISMO-COMANDO.md:663-668 | la variante medida: lista cerrada de los que no ejecutan, con `cmp`, `comm`, `xxd`, `nl`, `base64`, `strings`, `sha1sum` | Entra solo `cmp`: la lista crece cuando un comando la pide (guardia.py:2879-2880). Los demas (`comm`, `xxd`, `less`, `nl`, `tac`, `base64`, `strings`, `sha1sum`) se nombran en el informe final; matiz del auditor: `sha1sum` esta en `LECTOR_DE_METADATOS` (:1076) pero cae igual, porque :1794 va antes que :1796; `less` y `tac` no estan en la variante medida |
| GUARDIAS-CLAUDE.md | informe CERRADO de `trabajo/guardias-claude` | No lo nombra (0 apariciones de `cmp`, `_sin_prefijos`, `NO_EJECUTAN`, `_no_canonizable`): no describe lo que cambia, asi que no se toca (si hiciera falta, solo un recuadro) |
| GUARDIA-ALIAS.md:430-433 | `_canonica` pasa por cada literal de un guion, y por eso un `OSError` no niega | Se respeta: D1 no toca `_canonica`; solo evita que ciertos literales lleguen a ella |
| HISTORIA.md:17701-17702 | el recorte de PROJECT_STATE, asignado a la rama de la activacion de la 7a | Se mide en la entrega: 24.569 bytes tras la apertura; el cierre reescribe :84 y no anade lineas |
| CAPA-GENERADA.md:985 | «si la guardia niega, no se cambia de herramienta ni para comprobar» | Aplicado: `medir_windows.py` negado → decision 3, sin reescribirlo |

Otros matices del auditor que no cambian lo que se pide: «R6a.3 a R6a.8 escribiran MQL5 desde
Python» es, en la hoja, «portan codigo de Python» (HOJA:497-498); solo R6a.2 genera MQL5 desde
Python. La cifra «39 guiones / 10 con recorrido» no la publica ningun documento del repo; la
aproximacion del auditor con `git grep` da 44 y 14 por otro metodo; ni se confirma ni se desmiente,
y no cambia la decision del punto 2.

### f. Si no cabe para el sabado 14

Cabe: el cambio son dos piezas pequenas y los tests ya estan medidos. Si algo se alarga, recorto en
este orden: (1) los tests ROTO A PROPOSITO de las clausulas que no cambian nada en Windows (el
`os.name`); (2) los casos de F1 en `medir_g1.py` (quedaria F2, que es el que mide la CI de Linux), y
lo digo. No recorto D3, ni el ensayo del cierre (D7).

### El encargo frente al repo (auditor-encargo, 2026-11-12)

52 afirmaciones: 38 correctas, 2 incorrectas, 11 con matiz, 1 sin veredicto; 9 herencias. Las que
cambian algo, arriba: D1 abre huecos (a, b; decision 0); D5 tal cual rompe la suite y no mide F1 ni
F2 (d); F38y es F38w y `$'\r'` es otro mecanismo (e); `cmp` sobre dos ficheros de `docs/` de `main`
pasa hoy (a); el literal de F1 entero solo esta en `generar_capa.py:364` (CAPA-GENERADA.md:469 lo
trunca, y los anexos no traen motivos de la guardia); `GUARDIAS-CLAUDE.md` es un informe cerrado
(e). Los demas matices: «comentarios MQL5 `//+---` y `//|`» que D1 no cubre (hoy pasan porque no
llevan otra barra; un `//| docs/x |` futuro se negaria: fila `f1-mql5-pipe-con-barras`, decision
2); y el camino de las composiciones (`_compone_ruta_sensible` → `_exigir_ruta_del_codigo`), que D1
no toca: una f-cadena `// ...{x}/...` con `x` calculable sigue negada (fila
`f1-literal-359-fcadena`, con `p = 'x'`); en `generar_capa.py` real, `{perfil}` no se calcula y no
se dispara (decision 2).

### Lo que no pude medir

- **Como resuelve Windows `\\ localhost\C$\...`, `\\ x\..\C:\...` y `// a b/../...`**: la guardia nego
  `medir_windows.py` y no lo reescribi (decision 3).
- **Linux**: no hay Linux en la laptop. Lo de Linux sale del codigo, y lo medira la CI de `fix/`
  (donde `test_fase0_tabla` corre e imprime su tabla).

### Exposiciones

Ninguna: todo en un repo sintetico con ficheros falsos. Los `make check` de la rama, en la fila del
2026-11-12 de `HOLDOUT-EXPOSICIONES.md`.

## Lo que necesito que decidas

0. **D1 tal cual deja pasar h1-h8, que hoy se niegan (contradice D3).** Opciones: (a) D1d, solo en
   Windows: D1 + el tramo hasta el siguiente separador lleva un blanco + ningun fragmento de
   `SENSIBLES`; (b) D1a (D1 + `SENSIBLES`); (c) D1 tal cual, declarando h1-h8. Recomiendo (a): es
   la unica medida que deja pasar F1 (la copia real de `generar_capa.py`, :364 y :359) y niega los
   ocho; las dos clausulas son negativas (no es una gramatica de maquina) y no tocan
   `_sin_prefijos`. Coste de (b): h7 y h8 (la raiz por `\\ localhost\C$`, recorrida o no) pasan.
   Coste de (c): los ocho, y h1/h2 abren seguro.
1. **D5 tal cual rompe la suite y no mide F1 ni F2.** Opciones: (a) anadir F1 y F2 como casos de
   `medir_g1.py`, declararlos, cambiar la clave de `test_roto_la_comparacion_con_main` a la de F2, y
   subir la referencia en el mismo commit que el cambio de la guardia; (b) solo subir la referencia
   y vaciar, sin casos nuevos. Recomiendo (a): es lo que D5 quiere decir, y es la unica forma de que
   la comparacion caso a caso vea F1 y F2. Coste de (b): la declaracion queda vacia de contenido y
   el test roto a proposito falla por `KeyError`.
2. **Lo que D1 no cubre: `//|` con barras detras y la f-cadena `// ...{x}/...` calculable.**
   Opciones: (a) no se cubre ahora, se declara como residuo; (b) ampliar D1 a `//|` (un `|` no cabe
   en ninguna ruta de Windows) y al camino de las composiciones. Recomiendo (a): ningun guion real lo
   pide hoy (`generar_capa.py` pasa entero con D1d), y la lista solo crece cuando un caso la pide.
   Coste de (a): un generador futuro con `//| docs/x |` o con una f-cadena calculable vuelve a pedir
   «!».
3. **`medir_windows.py`, negado por la guardia.** Opciones: (a) lo lanzas con
   `! uv run --no-project python docs/validation/anexos/GUARDIA-FALSOS-POSITIVOS/medir_windows.py`
   y su salida va al anexo; (b) no se lanza. Recomiendo (a) si eliges (b) o (c) en el punto 0 (dice
   si h3-h8 son huecos reales o solo de papel); con (a) en el punto 0 no cambia nada. Coste de (b):
   el informe dice «no medido».
4. **h1b: un literal recortado al ejecutarse (`'x' + ruta[1:]`) ya pasa hoy.** Opciones: (a) se
   declara en el informe y en Technical Debt como limite conocido de la guardia, fuera de esta rama;
   (b) se intenta cerrar aqui. Recomiendo (a): no es de F1 ni de F2, ninguna variante lo empeora, y
   cerrarlo pide seguir el codigo al ejecutarse (otra rama, con su fase 0). Coste de (b): no cabe
   para el sabado.

Espero tu respuesta a la PARADA.

## Respuesta del consultor a la PARADA de la fase 0 (2026-11-12, 23:00)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/guardia-falsos-positivos (2026-11-12, 23:00). Cópiala tal cual al informe y al final del encargo, y aplícala punto por punto. Buena fase 0: tus cuatro correcciones al encargo quedan aceptadas.
>
> 0. (a) D1d, solo en Windows: un literal de un guion cuyos dos primeros caracteres son separadores seguidos de un espacio o un tabulador no se trata como ruta, solo si además el tramo hasta el siguiente separador lleva un blanco y el literal no lleva ningún fragmento de SENSIBLES. _sin_prefijos no cambia. Es la única variante medida que deja pasar la copia real de generar_capa.py (los dos literales, :359 y :364) y sigue negando h1-h8. Cada uno de h1-h8 entra como test que tiene que seguir negado, con su columna de Windows o Linux.
> 1. (a) F1 y F2 entran como casos de medir_g1.py; la clave del test que se rompe a propósito pasa a la de F2; y la referencia sube a stable/F38z-capa-generada en el mismo commit que el cambio de la guardia. Declara en CAMBIOS_DECLARADOS solo lo que esa referencia niega y la rama deja pasar.
> 2. (a) «//| docs/x |» y la f-cadena «// …{x}/…» con una variable calculable se declaran como residuo en el informe, con su porqué: ningún guion real lo pide hoy.
> 3. (b) No se lanza medir_windows.py: con D1d no hace falta. Dilo en el informe y no lo commitees si no se usa.
> 4. (a) h1b ('x' + ruta[1:]) se declara como límite conocido, y queda fuera porque ya pasa hoy con cualquier variante y la barrera es el código. Va al informe y, si GUARDIAS-CLAUDE.md tiene una sección de límites, también ahí. No va a Technical Debt, porque PROJECT_STATE está en 24.380 bytes.
> 5. Las correcciones al encargo: la deuda de « / » y </li> es de F38w, y $'\r' es otro mecanismo (la comilla ANSI-C de tokenizar). La línea de Technical Debt que entró con F38z se reescribe para el cierre así: F1 y F2 resueltos; «/» y la deuda de F38w siguen con «!», con el porqué del encargo; $'\r', aparte, sin cambios. Para la fila de ERRORES, del consultor: D1 tal como estaba escrita dejaba pasar ocho casos, contra su propia D3 (importa); D5 rompía test_roto_la_comparacion_con_main (menor); F38y en lugar de F38w (menor); $'\r' metido en el mismo mecanismo (menor).
> 6. Esta noche sigue sin parar: tests primero (rotos contra la guardia de stable/F38z), el cambio en guardia.py, medir_g1.py y la referencia, GUARDIAS-CLAUDE.md si describe lo que cambia, make check sellado en cada commit, push a fix/guardia-falsos-positivos con su CI, y el revisor. Solo paras si un caso de D3 o de h1-h8 pasa, si un test no rompe contra stable/F38z por el motivo que dice, o si la guardia niega algo legítimo (no cambias de vía: lo dejas para mi «!»).
> 7. El ensayo del cierre en un clon independiente (D7): si la guardia te deja hacer el git clone y su make check, hazlo. Si no, déjalo preparado con las órdenes exactas y lo lanzo yo por la mañana.
> Rama lista para revisión, NO cerrada.

## Aplicación de la respuesta (2026-11-12, noche)

Punto por punto:

- **0. D1d, solo en Windows: hecho.** `guardia.py`, junto a `_literales`: el bloque «F1: un
  comentario no es una ruta» con su porque, `_COMENTARIO`, `_tramo_lleva_blanco` y
  `_comentario_que_no_es_ruta` (las tres condiciones y `os.name == "nt"`), y una linea en el bucle
  de `analizar_codigo`, entre el `file:` y `_absoluta`. `_sin_prefijos`, `_canonica` y `_absoluta`
  no cambian (`git diff` de la rama: solo esas lineas y la entrada de `cmp`). h1-h8 entran como
  tests que tienen que seguir negados, cada uno con su sistema (tabla de casos, abajo).
- **1. medir_g1.py y la referencia: hecho**, en el mismo commit que el cambio de la guardia.
  `GUARDIA_DE_REFERENCIA = "stable/F38z-capa-generada"`; `CAMBIOS_DECLARADOS` vaciado y con dos
  entradas, `i1-f1-comentario` y `i2-f2-cmp` (las dos unicas que la referencia niega y la rama
  deja pasar, medido con la propia comparacion); casos nuevos `i1`, `i2` e `i3-cmp-protegido` (este
  sigue negado: «leer el contenido de <holdout>/...»); `test_roto_la_comparacion_con_main` borra
  `i2-f2-cmp`.
- **2. El residuo: hecho.** `//| docs/x |` y la f-cadena `// ...{x}/...` con una variable calculable
  siguen negados, con su test (`test_lo_que_d1d_no_cubre_sigue_negado`), y se declaran aqui: ningun
  guion real lo pide hoy (`generar_capa.py` pasa entero). La f-cadena calculable va por las
  composiciones (`_compone_ruta_sensible` → `_exigir_ruta_del_codigo`), que D1d no toca.
- **3. `medir_windows.py`: no se lanza.** Con D1d no hace falta. Ya estaba en el commit de la fase 0
  (`dce4004e`); sale del repo con `git rm` en el commit de esta fase, y la fase 0 lo nombra solo
  como lo que se intento y la guardia nego.
- **4. h1b: declarado** como limite conocido aqui (fase 0, §b) y en `GUARDIAS-CLAUDE.md`, §1.7 «Lo
  que no ve», con un RECUADRO DE CORRECCION (es un informe cerrado: el cuerpo queda intacto). No va
  a Technical Debt.
- **5. Las correcciones y las lineas del cierre**: en «Lineas para el cierre», abajo.
- **6. Sin parar: en curso** (tests primero, el cambio, `make check` en cada commit, `fix/`, el
  revisor).
- **7. El ensayo del cierre**: en su seccion, abajo.

### Tests primero: lo que rompe contra la guardia de stable/F38z

Los tests se escribieron con la guardia del arbol igual byte a byte a la de `stable/F38z`
(`git diff --stat stable/F38z-capa-generada -- .claude/hooks/` vacio) y se corrieron ANTES de
tocarla: 15 fallos, cada uno por el motivo que dice *(B4 del revisor: el test de D6,
`test_f1_el_literal_no_llega_a_absoluta_ni_tarda`, se escribio DESPUES de esa corrida y no esta en
el anexo; con la referencia falla por la misma negativa que `test_la_referencia_niega_f1_por_no_canonizar`,
que usa la misma entrada y si corre en la suite)*
(`anexos/GUARDIA-FALSOS-POSITIVOS/rotos-contra-F38z-SALIDA.txt`):

- los cinco de F1 (la copia de `generar_capa.py`, :364, :359, tabulador, barras invertidas):
  «la ruta `// ...` no se puede canonizar»;
- los tres de F2: «ejecutar `cmp`: la guardia no sabe con que se ejecuta ...»;
- `cmp` con un fichero protegido: la referencia tambien lo niega, pero por `R_EJECUCION`
  («ejecutar `cmp`»); el test pide `R_HOLDOUT`, la regla de la lectura (D2);
- `test_la_referencia_es_stable_f38z`: la referencia era `stable/F38k-margen-pendiente`;
- los cinco ROTO A PROPOSITO: con la referencia no existen las piezas que rompen
  (`_tramo_lleva_blanco`, `_comentario_que_no_es_ruta`: `AttributeError`; `cmp` no esta en
  `NO_EJECUTAN`: `KeyError`) o la referencia ya niega lo que el test quiere ver pasar.

Los que aseguran lo que sigue negado (h1-h8, D3, el residuo) pasan con las dos guardias, que es lo
que tienen que hacer. Y dos tests dejan fijado DENTRO de la suite lo que la referencia decidia:
`test_la_referencia_niega_f1_por_no_canonizar` (solo Windows) y
`test_la_referencia_niega_f2_por_ejecutar` cargan la guardia del tag y exigen su negativa con su
motivo.

**D6, medido**: `test_f1_el_literal_no_llega_a_absoluta_ni_tarda` — los dos literales de F1 no
llegan a `_absoluta` (ni a `realpath`), y `decidir()` sobre la copia de `generar_capa.py` tarda
0,14 s. Los `//+---`, `//| ...` y `// ` de su cabecera SI llegan a `_absoluta`, como con la
referencia: no son de F1 (no llevan blanco en el tramo), ya pasaban y no tardan (el matiz 34 del
auditor).

**Una trampa de la medida, resuelta en el test**: el temporal de pytest en Windows lleva `AppData\`,
que casa con el fragmento `data\` de `SENSIBLES` y haria negar h7 y h8 por el fragmento y no por la
condicion del blanco. La fixture `base` pone el repo inventado en una carpeta nueva de la del
usuario cuando el temporal lleva un fragmento, y la borra al acabar. La primera version la borraba
con `ignore_errors=True`, que en Windows deja la carpeta entera sin avisar (los objetos de git son
de solo lectura): quedaron 130 carpetas `gfp-*` en la carpeta del usuario, borradas a mano; ahora
`_borrar` quita el «solo lectura» y comprueba que la carpeta ya no existe.

## Cada caso, con su test y sus dos decisiones (hasta la PARADA 2)

*Tabla de antes de la PARADA 2 y del aplazamiento de F1. El estado final, con los casos de las dos
pasadas del revisor, en «Cada caso, estado final», mas abajo.*

`F38z` es la guardia de `stable/F38z-capa-generada` (la de `main`); `rama`, la de esta rama. «W»
solo Windows (en Linux el test salta); «W+L» los dos. Los tests, en
`tests/unit/test_guardia_falsos_positivos.py` salvo que se diga.

| caso | test | F38z | rama | sistema |
|---|---|---|---|---|
| F1: la copia cambiada de `generar_capa.py` (:364 y :359) | `test_f1_la_copia_cambiada_de_generar_capa_pasa` | niega (no canoniza) | pasa | W |
| F1: :364 solo | `test_f1_un_comentario_de_un_guion_nuevo_pasa[364]` | niega | pasa | W |
| F1: :359, la f-cadena con un parametro | `...[359-fcadena]` | niega | pasa | W |
| F1: `//` + tabulador | `...[tabulador]` | niega | pasa | W |
| F1: `\\ ` | `...[barras-invertidas]` | niega | pasa | W |
| D6: los literales de F1 no llegan a `_absoluta`; 0,14 s | `test_f1_el_literal_no_llega_a_absoluta_ni_tarda` | niega | pasa | W |
| F2: `cmp` de dos ficheros nuevos de `docs/` | `test_f2_cmp_de_dos_ficheros_que_no_son_guiones_pasa` | niega (ejecutar) | pasa | W+L |
| F2: `cmp -s` | idem | niega | pasa | W+L |
| F2: el nombre con `=` del origen de G.6 | idem | niega | pasa | W+L |
| cmp con un protegido (2.º, 1.º, absoluto) y `diff` con uno | `test_f2_cmp_con_un_fichero_protegido_se_niega_por_la_lectura` | niega (`R_EJECUCION`; diff `R_HOLDOUT`) | niega (`R_HOLDOUT`) | W+L |
| h1 `"// <prot>"[3:]` | `test_h_los_casos_de_windows_siguen_negados[h1-recorte]` | niega | niega | W |
| h1c `"// a b/<prot>"[6:]` | `...[h1c-recorte-blanco-interior]` | niega | niega | W |
| h2 `.lstrip('/ ')` | `...[h2-lstrip]` | niega | niega | W |
| h3 `// x/../<raiz>/<prot>` | `test_h3_el_punto_punto_sigue_negado` | niega | niega | W+L |
| h4 `\\ localhost\C$\...\<prot>` | `...[h4-espacio-localhost]` | niega | niega | W |
| h5 con tabulador | `...[h5-tab-localhost]` | niega | niega | W |
| h6 con el nombre del equipo | `...[h6-espacio-equipo]` | niega | niega | W |
| h7 la raiz por `\\ localhost`, recorrida | `...[h7-raiz-recorre]` | niega | niega | W |
| h8 la raiz por `\\ localhost`, `os.stat` | `...[h8-raiz-sin-recorrer]` | niega | niega | W |
| D3: `//host/share/...` y `\\host\share\...` en un guion nuevo | `test_d3_un_recurso_de_red_sin_blanco_sigue_negado` | niega | niega | W |
| D3: un guion nuevo que nombra o recorre lo protegido | `test_d3_un_guion_nuevo_que_nombra_o_recorre_lo_protegido_sigue_negado` | niega | niega | W+L |
| D3: los alias y no canonizables de `test_guardia_alias.py` (:183-199 por `_formas`, :439-463, :512-520) y `file://` de `test_guardia_g1.py` (:622-631) | esos mismos tests, sin cambiar | niega | niega | W (salvo los de dos sistemas) |
| residuo: `//\| ver docs/x \|` | `test_lo_que_d1d_no_cubre_sigue_negado[barra-vertical]` | niega | niega | W |
| residuo: f-cadena `// ...{p}` con `p` calculable | `...[fcadena-calculable]` | niega | niega | W |
| h1b `'x' + <prot>[1:]` (limite conocido) | — (declarado, no se asegura un hueco) | pasa | pasa | W+L |
| la referencia negaba F1 por no canonizar | `test_la_referencia_niega_f1_por_no_canonizar` | — | — | W |
| la referencia negaba F2 por ejecutar | `test_la_referencia_niega_f2_por_ejecutar` | — | — | W+L |
| la comparacion caso a caso (`medir_g1.py`, `i1`-`i3`) | `test_guardia_g1.py::test_la_comparacion_caso_a_caso_con_la_guardia_de_main` | — | `i1` y `i2` declarados; `i3` niega en las dos | W (i1) / W+L (i2, i3) |

ROTO A PROPOSITO (la rama, Windows salvo los de `cmp`): sin la clausula de `SENSIBLES`, h1c pasa;
sin la del blanco, h7 y h8 pasan; sin la condicion entera, F1 se niega; sin `cmp` en
`NO_EJECUTAN`, F2 se niega (W+L); con `cmp` en `SIN_LECTURA_DE_RUTAS`, el protegido pasa (W+L). La
condicion `os.name == "nt"` no tiene test roto: quitarla no cambia nada en Windows, y en Linux solo
haria saltar literales que la referencia ya dejaba pasar (en Linux `// x` es `/ x`, fuera de la
raiz); se dice aqui en vez de fingir un test.

## Los demas lectores con el mismo fallo (punto 2 del encargo)

Fuera de `NO_EJECUTAN`, y por tanto leidos como si ejecutaran un fichero nuevo que reciben: `comm`,
`xxd`, `less`, `nl`, `tac`, `base64`, `strings` y `sha1sum` (este esta en `LECTOR_DE_METADATOS`,
guardia.py:1076, pero cae igual porque la condicion de :1794 va antes que :1796). No entran: la
lista solo crece cuando un comando la pide (guardia.py:2879-2880). `fc` no es un lector: en Git
Bash es un comando interno que vuelve a ejecutar el historial (lo niega `BUILTINS_NO_ADMITIDOS`).

## El encargo, punto por punto

| Punto | Lo pedido | Hecho |
|---|---|---|
| 0 | Base comprobada; abrir con abrir-rama; contrato con tramo, permitidas y protegidas | Hecho (Apertura); contrato en `6a310dc8` |
| 1 | F1 y F2, sin abrir ningun hueco | **F2 hecho; F1 aplazado**: D1 abria h1-h8 (fase 0); D1d lo rodearon B1 y B2 (primera pasada del revisor); D1d con los dos arreglos de la PARADA 2 lo rodearon R1-R4 (segunda pasada). Respuesta a la PARADA 2, punto 4: la guardia vuelve a la de stable/F38z para esos literales |
| 2 | `/` de compilar.py, F38w, worktree add, los demas lectores y D: fuera | Fuera; los lectores, nombrados arriba; la atribucion F38y→F38w y `$'\r'` como otro mecanismo, corregidas (punto 5 de la respuesta) |
| 3, D1 | En negativo, en `analizar_codigo`, `_sin_prefijos` intacto | Se hizo (D1d) y se aplazo: el diff final de `guardia.py` contra stable/F38z es solo la entrada de `cmp` |
| D2 | `cmp` en `NO_EJECUTAN`, sus argumentos como lectura | Hecho |
| D3 | Ningun caso que hoy se niega deja de negarse | Hecho y con test: h1-h8, B1-B2 y R1-R4 niegan en la rama (estado final); h1b ya pasaba (limite conocido) |
| D4 | En memoria, repo sintetico, a trozos, W o L por caso | Hecho; de `cmp`, el nombre de G.6 y dos ficheros nuevos de `docs/` (con dos de `main` ya pasaba hoy) |
| D5 | Referencia a F38z, lista vaciada, F1 y F2 declarados | Hecho con F1 y F2 como casos nuevos de `medir_g1.py`; al aplazar F1, solo `i2-f2-cmp` queda declarado (`i1` niega en las dos) |
| D6 | F1 solo Windows; no tarda | Se midio (0,14 s; no llegaba a `_absoluta`); con F1 aplazado, su test es `xfail` estricto |
| D7 | Ensayo del cierre en un `git clone` | La guardia niega `git clone`: preparado para Aleks, en el estado final (seccion siguiente) |
| 4 | Nada fuera de la guardia, sus tests y lo nombrado | `git diff main --stat`: la guardia, dos tests, `medir_g1.py`, `GUARDIAS-CLAUDE.md` (recuadro), `HOLDOUT-EXPOSICIONES.md` (dos filas), el informe, sus anexos, el encargo, el contrato, PROJECT_STATE y HISTORIA |
| 5 | Fase 0 y PARADA | Hecho (`dce4004e`) |
| 6 | Tests primero, el cambio, la referencia, make check, CI de `fix/`, revisor, ensayo | Hecho; el ensayo, para Aleks (D7) |
| 7 | El informe | Este |
| 8 | Revisor con los ejes extra | Dos pasadas enteras, pegadas al final |
| R1.0-5 | Respuesta a la PARADA 1 | Aplicada (seccion «Aplicacion de la respuesta») |
| R2.0-3 | Respuesta a la PARADA 2, puntos 0-3 | Aplicados en `5f757439`, y retirados con F1 al aplicar el punto 4 (salvo los tests de lo que sigue negado y el de B3) |
| R2.4 | El revisor entero; si rompe F1, F1 sale | Rompio F1 (R1-R4, medidos): F1 aplazado; la rama se queda con F2 y G.6 |
| R2.5 | Las ordenes de D7 en el estado final | En «El ensayo del cierre» |
| R2.6 | «Rama lista para revision, NO cerrada», con commits, runs, revisor y F1 | En «Estado» |

Desviaciones: F1 no entra (aplazado por la respuesta a la PARADA 2, punto 4); D1 se aplico como
D1d (decidido en la PARADA) antes de aplazarse; `medir_windows.py` se commiteo en la
fase 0 y salio del repo en la siguiente (punto 3); la fixture que borraba con `ignore_errors` dejo
130 carpetas `gfp-*` en la carpeta del usuario antes de arreglarla (borradas). Y las negativas de la
guardia a comandos mios (todas con la forma que ella propone, ninguna del objeto de la rama): tres
`uv run` encadenados tras otra orden, un `git ls-files` desde la raiz (ADR-0088), un `pytest -o` que
no hacia falta, y `git clone` (D7). La guardia de Claude Code NO nego nada legitimo de la rama
salvo `medir_windows.py` (fase 0) y `git clone`.

## Lineas para el cierre (simuladas)

- **HOJA-DE-RUTA.md, G.6**: «- **Hecho cuando:** su test que la rompe a propósito.» pasa a decir
  que esta HECHA en `trabajo/guardia-falsos-positivos` (`cmp` en `NO_EJECUTAN`;
  `test_roto_sin_cmp_en_no_ejecutan`), con la forma de las demas entradas hechas de la hoja.
- **PROJECT_STATE.md, Technical Debt**, la linea que entro con F38z (hoy :84), reescrita. El punto
  5 de la respuesta a la PARADA 1 decia «F1 y F2 resueltos»; con F1 aplazado (PARADA 2, punto 4),
  solo F2 sale, y la linea no lo nombra (PROJECT_STATE es el presente):

  > - La guardia niega a un guion nuevo dos falsos positivos, que lanza Aleks con «!»: un texto
  >   que empieza por `//` y un blanco, como ruta de red (F1, aplazado en
  >   `trabajo/guardia-falsos-positivos`: ninguna condicion medida aguanta), y un literal que solo
  >   es separadores, como el `/` de `compilar.py`, por el mismo mecanismo que « / » y `</li>` de la
  >   linea de F38w de abajo (CAPA-GENERADA.md, «La guardia»).

  La de F38w (hoy :152, con `$'\r'`) queda sin cambios (punto 5 de la respuesta a la PARADA 1).
- **PROJECT_STATE.md, tamano**: 24.612 bytes en la rama (el ultimo commit); con la linea
  reescrita, 24.787 (simulado en memoria, +175); el cierre devuelve Current Branch y Current
  Feature a lo de `main` (24.380 hoy en `main`): queda hacia 24.555, por debajo del tope de 25.000.
  No hace falta recortar.
- **ERRORES-RECURRENTES.md**, la fila del consultor (punto 5 de la PARADA 1): D1 tal como estaba
  escrita dejaba pasar ocho casos, contra su propia D3 (importa); D5 rompia
  `test_roto_la_comparacion_con_main` (menor); F38y en lugar de F38w (menor); `$'\r'` metido en el
  mismo mecanismo (menor). Y lo que la rama aprendio despues, para la misma fila si el consultor
  quiere: D1d (propuesta mia, aceptada) la rodearon B1 y B2 en la primera pasada del revisor, y sus
  arreglos, R1-R4 en la segunda: una condicion que deja de leer como ruta parte de un literal la
  rodea un recorte o un `cd` al ejecutarse (importa).
- **HISTORIA.md**, el registro del cierre, como siempre. Siguiente tag: `stable/F39a-...` (F38 acaba
  en z).

## El ensayo del cierre (D7), preparado para Aleks

La guardia niega `git clone` («subcomando fuera de la lista cerrada»), como en `trabajo/guardia-g1`
(GUARDIA-G1.md §13.7). Las ordenes, en el orden de aquel ensayo; «!» las lanza Aleks, el resto la
sesion. Antes, comprobado: ni el `Makefile` ni sus guiones llevan `push`.

| # | Orden | Quien |
|---|---|---|
| 1 | `git clone "C:/Users/USER/Desktop/Bot v3" C:/cm/gfpc` | Aleks, «!» |
| 2 | `git -C C:/cm/gfpc switch trabajo/guardia-falsos-positivos` y `git -C C:/cm/gfpc switch main` | sesion |
| 3 | `git -C C:/cm/gfpc remote remove origin` | Aleks, «!» |
| 4 | `git -C C:/cm/gfpc config user.name ensayo` y `git -C C:/cm/gfpc config user.email ensayo@ejemplo.invalid` | Aleks, «!» |
| 5 | en la rama: `git rm contrato.yaml` y commit, como el `chore(cierre)` | sesion |
| 6 | `switch main` y `merge --no-ff trabajo/guardia-falsos-positivos` | sesion |
| 7 | `tag -a stable/F39a-guardia-falsos-positivos` (solo en el clon) | sesion |
| 8 | `PROJECT_STATE.md` del clon con las cabeceras del cierre (rama `main`, ninguna abierta) y `git add` | sesion |
| 9 | `cd C:/cm/gfpc && make check > C:/cm/make-check-merge.log 2>&1` | Aleks, «!» |
| 10 | leer el log (exit 0, ningun `failed`; *corregido en «El ensayo del cierre (D7), hecho»: `make check` sella igual sin contrato, solo que en el clon nadie exige el sello*) y quitar el clon: `rm -rf C:/cm/gfpc` | sesion lee; Aleks, «!», borra |

Las ordenes valen para el estado final de la rama (el ultimo commit, con F1 aplazado): el paso 2
trae la rama tal como este en `C:/Users/USER/Desktop/Bot v3` cuando se lance el paso 1. Lo que el
ensayo tiene que ver en verde, en un `main` que se mueve de verdad: que
`test_la_referencia_es_un_tag_y_no_es_esta_guardia` y la comparacion caso a caso siguen midiendo
tras el merge (la referencia es el tag F38z, no `main`), y que los tests de la rama pasan sobre el
arbol fusionado.

## La CI de Linux por fix/

`git push origin trabajo/guardia-falsos-positivos:refs/heads/fix/guardia-falsos-positivos` (la
sesion; el clasificador no lo nego). Run **43366719378**, `headSha` `f9888a03af5b62838f1c248801dea72333a2108d`
(`gh run view --json`), rama `fix/guardia-falsos-positivos`: **failure solo por el fallo aceptado**
(`RITUAL.md`, «Antes del merge: la CI de Linux»): `tests/unit/test_cli.py::test_state_check_ok_on_real_repo`,
«PROJECT_STATE declara la rama 'trabajo/guardia-falsos-positivos'; la rama actual es
'fix/guardia-falsos-positivos'». **1 failed, 3427 passed, 70 skipped**; lint «All checks passed!».
La CI trae los tags (`git fetch --tags --force`, el workflow), asi que las comparaciones con la
referencia corrieron de verdad en Linux. Los saltados son los que necesitan `data/` y los de solo
Windows (F1 y sus casos, h1-h2 y h4-h8, los de `test_guardia_alias.py`).

`make check` de los commits de la rama, en la laptop:

| commit | que | resultado |
|---|---|---|
| `6a310dc8` | apertura | exit 0, 3465 passed, SELLO `66f3230f`, 1284 s, pico 315 MiB |
| `dce4004e` | fase 0 | exit 0, 3466 passed, SELLO `ce1c7169`, 1304 s, pico 313 MiB |
| `f9888a03` | fase 1 (la guardia, los tests, la referencia) | exit 0, 3498 passed, SELLO `090c2de9`, 1337 s, pico 317 MiB |
| `32316acf` | el informe: casos, encargo, cierre, ensayo, CI | exit 0, 3498 passed, SELLO `a9a587ba`, 1312 s, pico 317 MiB |
| `55d41a02` | el revisor (primera pasada) y la PARADA 2 | exit 0, 3504 passed, 4 xfailed, SELLO `867a8f29`, 1359 s, pico 320 MiB |
| `5f757439` | la respuesta a la PARADA 2 (B1, B2) | exit 0, 3516 passed, SELLO `0c5318da`, 1082 s, pico 316 MiB |
| (el ultimo) | F1 aplazado, la segunda pasada del revisor | en el mensaje de entrega |

La CI de `5f757439`: run **43379762621**, failure solo por el fallo aceptado (el mismo
`test_state_check_ok_on_real_repo`), **1 failed, 3428 passed, 87 skipped**. La del ultimo commit,
en el mensaje de entrega (un informe no puede llevar el run de su propio commit).

## Lo que se hizo con los hallazgos del revisor

El informe del revisor (opus, 2026-11-13, sobre `32316acf`), pegado tal cual al final. Eje (a): sin
hallazgos. Eje (b): 2 bloquea, 3 importa, 2 menor.

- **B1 (bloquea): confirmado, PARADA 2.** Un blanco DETRAS del nombre de maquina
  (`\\ localhost \C$\<raiz>`, recorrida o con `os.stat`, y con tabulador) pasa en la rama y
  `stable/F38z` lo niega. Tests nuevos: `test_revisor_las_variantes_siguen_negadas[b1-*]` (en la
  rama, `xfail` estricto marcado «PARADA 2») y `test_revisor_la_referencia_niega_las_variantes`
  (la referencia los niega, en verde). Con un blanco detras y la ruta protegida entera (`b1-h4`) la
  rama SI niega: el literal lleva un fragmento de `SENSIBLES`.
- **B2 (bloquea): confirmado, PARADA 2.** `"// a b/<fichero de ficheros_con_ocultos.txt>"[7:]`
  pasa en la rama y la referencia lo niega (no canoniza). Medido con un `docs/oculto-SALIDA.txt`
  listado en el `ficheros_con_ocultos.txt` del repo inventado. Mismos dos tests. Y el comentario de
  `guardia.py` («un `"// <ruta protegida>"[3:]` se sigue mirando») afirma mas de lo que el codigo
  sostiene: solo vale si la ruta lleva fragmento; se corrige con el arreglo que decida el consultor.
- **B3 (importa): cierto, se declara.** `cmp` en `NO_EJECUTAN` tiene dos efectos mas que el informe
  no decia: (1) una f-cadena o una suma que empieza por `cmp ` deja de contar como composicion de C
  (`_empieza_por_un_programa`), igual que `diff`; (2) `cmp` entra en `PROGRAMAS_DE_DATOS` de la
  regla de la CI. Ninguno abre nada: `cmp` no ejecuta, y (1) es el trato que ya tiene `diff`. Tras la
  PARADA 2, un test que lo fije (`cmp` y `diff` igual en `_es_composicion`).
- **B4 (importa): cierto, corregido el texto** (§«Tests primero»): el test de D6 se escribio despues
  del anexo de los rotos; su fallo con la referencia lo prueba `test_la_referencia_niega_f1_por_no_canonizar`,
  con la misma entrada.
- **B5 (importa): cierto.** La CI de `fix/` es de `f9888a03`; el ultimo push ira con el ultimo
  commit de la rama, tras la PARADA 2.
- **B6 (menor): corregido**: la tabla se llama «El encargo, punto por punto».
- **B7 (menor): se declara.** La fixture `base` escribe en la carpeta del usuario cuando el
  temporal de pytest lleva un fragmento de `SENSIBLES`; si el proceso muere de golpe deja `gfp-*`
  (hoy, 0).

## PARADA 2 (2026-11-13): dos variantes que la rama deja pasar y stable/F38z niega

Punto 6 de la respuesta: «Solo paras si un caso de D3 o de h1-h8 pasa». B1 es una variante de
h7/h8 y B2 de h1c; los dos los niega la referencia. Paro.

Arreglos medidos en memoria, simulados con `monkeypatch` sin tocar `guardia.py`
(`anexos/GUARDIA-FALSOS-POSITIVOS/medida_parada2.py`, que corrio como test temporal y se saco de
`tests/`; su salida, `parada2-windows-SALIDA.txt`):

| variante | B1 (3 casos) | B2 | h1-h8 | F1 (la copia de `generar_capa.py` y 3 literales) | `decidir` de la copia |
|---|---|---|---|---|---|
| la rama hoy | pasan | pasa | niegan | pasan | 0,16 s |
| B1: el tramo sin blancos a los DOS lados | niegan | pasa | niegan | pasan | 0,16 s |
| B1 + b: ademas, cada sufijo tras un separador se mira como ruta (fichero protegido, o carpeta que lo contiene, recursiva) | niegan | niega | niegan | pasan | 0,20 s |
| B1 + d: el sufijo desde CADA posicion | niegan | niega | niegan | **niega F1**: el «.» final del literal de :364 es la raiz | 0,30 s |

Lo que deja B1 + b: un recorte a mitad de nombre (`"// a b/x<ruta>"[8:]`), que es la clase de h1b
(`'x' + ruta[1:]`), que ya pasa con la referencia y quedo como limite conocido (punto 4).

### Lo que necesito que decidas (PARADA 2)

0. **B1.** Opciones: (a) el tramo se mira sin blancos a los dos lados (`strip` en vez de `lstrip`);
   (b) otra forma. Recomiendo (a): solo endurece, cierra los tres casos medidos y F1 sigue pasando.
   Coste de (b): ninguno medido que la mejore.
1. **B2.** Opciones: (a) B1 + b: para un literal de F1, cada sufijo tras un separador se mira como
   una ruta (fichero protegido, o carpeta que lo contiene, recursiva), y si alguno lo es, el literal
   se trata como hoy; (b) se declara dentro del limite de h1b; (c) F1 sale de la rama y queda solo
   F2. Recomiendo (a): cierra B2 y todo recorte que caiga en un separador, y deja solo el recorte a
   mitad de nombre, que es h1b y ya pasa hoy; F1 sigue pasando (0,04 s mas). Coste de (b): B2 pasa
   y la referencia lo niega, contra D3. Coste de (c): F1 sin resolver para R6a.
2. **B3-B7**, que no paran: lo de arriba (B3 declarado y con test tras la PARADA; B4 y B6
   corregidos; B5 con el ultimo commit; B7 declarado). Opciones: (a) asi; (b) otra cosa.
   Recomiendo (a).

Tras la respuesta: el arreglo con sus tests (los `xfail` pasan a tests normales y rompen contra la
rama de hoy), `make check`, el push a `fix/` con el ultimo commit y una pasada corta del revisor
sobre el arreglo.

Espero tu respuesta a la PARADA 2.

## Respuesta del consultor a la PARADA 2 (2026-11-13, 01:15)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA 2 de trabajo/guardia-falsos-positivos (2026-11-13, 01:15). Cópiala tal cual al informe y al final del encargo, y aplícala.
>
> 0. B1: (a). En la condición de F1, los blancos del tramo hasta el siguiente separador se quitan por los dos lados antes de mirar si queda un blanco dentro.
> 1. B2: (a). En un literal de F1, lo único que se exime es leer su cabeza como ruta de red; cada sufijo tras un separador se mira como ruta con las comprobaciones de siempre. Lo que queda (un recorte a mitad de un nombre) es la clase de h1b, que ya pasa con la guardia de stable/F38z: decláralo junto a h1b, con la medida que lo demuestra contra stable/F38z.
> 2. B3 a B7: (a), como están contestados en el informe.
> 3. Los dos xfail estrictos pasan a tests normales que tienen que seguir negados. make check sellado, commit, push a fix/guardia-falsos-positivos con el último commit y su CI (solo el fallo aceptado).
> 4. El revisor otra vez, una pasada entera, no corta, con un alcance más: intentar romper F1 (literales que empiecen por separadores y blanco, con recortes, sufijos, f-cadenas y mezclas de / y \) contra la guardia de stable/F38z. Si encuentra un caso que stable/F38z niega y la rama deja pasar, no paras: F1 sale de la rama (vuelves a la condición de stable/F38z para esos literales, con sus tests como xfail estricto documentado y lo medido al informe, como «F1, aplazado: ninguna condición medida aguanta»), y la rama se queda con F2 y G.6. Después, make check, push y CI.
> 5. El ensayo del cierre (D7): deja en el informe las órdenes exactas para que las lance yo con «!», en el estado final de la rama.
> 6. Al terminar: «Rama lista para revisión, NO cerrada», con la tabla de commits, los runs, el resultado del revisor y si F1 entró o se aplazó.

## Aplicación de la respuesta a la PARADA 2 (2026-11-13)

- **0. B1: hecho.** `_tramo_lleva_blanco` quita los blancos del tramo por los DOS lados (`strip`)
  antes de mirar si queda uno dentro.
- **1. B2: hecho.** En un literal de F1 solo se exime la cabeza: `_sufijos_tras_separador` da cada
  sufijo tras un separador (con `/` o `\`), y cada uno pasa por `_mirar_literal`, que son las
  comprobaciones de siempre, sacadas a una funcion del bucle de `analizar_codigo` sin cambiar lo
  que hacen (fichero protegido; carpeta que lo contiene, recursiva si el codigo recorre). Un
  sufijo no suma a `directorios`: la regla de «recorre y nombra algo sensible» no se debilita por
  un trozo de comentario. Medido: la copia de `generar_capa.py` sigue pasando; B2 (con `/` y con
  `\`) y una carpeta sin fragmento que contiene el holdout, recortada y recorrida, niegan.
  **El residuo, declarado junto a h1b** (aqui y en el recuadro de `GUARDIAS-CLAUDE.md` §1.7),
  con la medida contra stable/F38z (`test_el_residuo_de_f1_es_la_clase_de_h1b`, sobre el mismo
  fichero oculto del repo inventado):

  | | `'x' + oculto` `[1:]` (h1b) | `"// a b/x" + oculto` `[8:]` (el residuo) |
  |---|---|---|
  | stable/F38z | PASA | niega |
  | la rama | PASA | PASA |

  La clase (leer un fichero protegido con un literal que el codigo recorta al ejecutarse) ya pasa
  con la referencia; el residuo es otra forma de lo mismo. Si la ruta lleva un fragmento de
  `SENSIBLES`, el residuo tambien niega en la rama (lo fija `test_roto_sin_la_clausula_de_sensibles`).
- **2. B3-B7: como estan contestados.** El test de B3 entra: `test_b3_cmp_como_diff_en_las_composiciones`.
- **3. Los `xfail` pasan a tests normales**: `test_revisor_las_variantes_siguen_negadas` (siete
  casos, con dos nuevos: B2 con `\` y la carpeta recorrida) y su gemelo contra la referencia. Los
  cuatro que eran `xfail` fallaban con la guardia de `55d41a02` (el `make check` de ese commit:
  «3504 passed, 4 xfailed», estrictos) y pasan con la de ahora. Dos ROTO A PROPOSITO nuevos: sin
  los sufijos, B2 pasa (`test_roto_sin_los_sufijos`); con el tramo sin quitar los blancos de
  detras, B1 pasa (`test_roto_el_tramo_sin_quitar_los_blancos_de_detras`). Y
  `test_roto_sin_la_clausula_de_sensibles` cambia de caso: h1c ya lo niegan los sufijos, asi que
  mide el recorte a mitad de nombre de una ruta con fragmento, que solo ve esa clausula.
- **Una medida que no entra como caso**: `'// a b/docs'[7:]` recorrido pasa en la rama y la
  referencia lo niega, pero no es material protegido para la politica: un `'docs'` literal con
  `rglob` ya pasa con stable/F38z (la politica no para recorrer una carpeta por un fichero oculto
  dentro; `GUARDIAS-CLAUDE.md` §1.7). El caso de carpeta que entra es `knowledge` (contiene el
  holdout, sin fragmento en el nombre).
- **4, 5 y 6**: el revisor entero con el alcance nuevo, el ensayo y el cierre del informe, abajo.

`pytest` de los ficheros de la guardia (los cinco del contrato, el nuevo y `test_revisor.py`):
1001 passed.

## F1, aplazado: ninguna condición medida aguanta (2026-11-13)

La segunda pasada del revisor (opus, sobre `5f757439`, pegada al final) intento romper F1 contra la
guardia de stable/F38z y propuso cuatro casos que, por el codigo, esa guardia niega y la de la rama
dejaba pasar. **Medidos** con `decidir`, en el repo inventado (tests `test_r_la_referencia_niega`
y `test_r_siguen_negados`, con la guardia de `5f757439`):

| caso | guion (en linea, `uv run python -c`) y directorio de trabajo | stable/F38z | rama en `5f757439` |
|---|---|---|---|
| R1 | `open('// estrategia del trader/sesiones/x.txt'[3:])`, desde `corpus/` | niega («la ruta `// estrategia del trader/sesiones/x.txt` no se puede canonizar») | **pasa** |
| R2 | `os.walk('// r b/knowledge'[3:])`, desde la carpeta que contiene el repo `r b` | niega («la ruta `// r b/knowledge` no se puede canonizar») | **pasa** |
| R3 | `Path('\\ local host\C$\<raiz>'.replace(' ', '', 2)).rglob('*')`, desde la raiz | niega (no canoniza) | **pasa** |
| R4 | `Path('// a b/x//localhost/C$/<raiz>'[8:]).rglob('*')`, desde la raiz | niega (no canoniza) | **pasa** |

La causa es la del revisor (B-1): los sufijos de un literal de F1 se resuelven contra el directorio
de trabajo, y eso solo coincide con la ruta que se abre si la cabeza no es una carpeta de verdad y
la cola no es absoluta; un `cd` o un `C$` lo rompen. R1-R3 no son un recorte a mitad de un nombre;
R4 corta en la frontera de un nombre. Por el punto 4 de la respuesta a la PARADA 2, **F1 sale de la
rama**:

- `guardia.py` vuelve a la de stable/F38z para esos literales: `git diff stable/F38z-capa-generada
  -- .claude/hooks/guardia.py` es solo la entrada de `cmp` en `NO_EJECUTAN` (4 lineas). Salen
  `_COMENTARIO`, `_tramo_lleva_blanco`, `_sufijos_tras_separador`, `_comentario_que_no_es_ruta` y
  `_mirar_literal` (el bucle de `analizar_codigo` vuelve a ser el de stable/F38z, byte a byte).
- Los tests de F1 que aseguran que pasa (la copia de `generar_capa.py`, D6, y los cuatro literales)
  quedan como `xfail` estricto, con el motivo «F1, aplazado: ninguna condicion medida aguanta»: si
  una rama futura los hace pasar, la suite lo dice. Los ROTO A PROPOSITO de las piezas de F1 salen
  con ellas (sin la pieza no hay nada que romper). Se quedan, como bateria para una condicion
  futura, todos los que aseguran lo que sigue negado: h1-h8, B1-B2, R1-R4, D3 y el residuo.
- `medir_g1.py`: `i1-f1-comentario` se queda como caso (niega en las dos guardias) y sale de
  `CAMBIOS_DECLARADOS`, que queda solo con `i2-f2-cmp`.
- El recuadro de `GUARDIAS-CLAUDE.md` §1.7 dice ahora el limite (h1b) y por que F1 se aplazo.
- La linea de Technical Debt del cierre deja F1 como deuda que lanza Aleks con «!» (seccion «Lineas
  para el cierre»).

Lo que un intento futuro de F1 tiene que saber (de las tres versiones medidas): el literal entero no
llega a nada local (es un recurso de red con un blanco en el servidor), pero el codigo puede
recortarlo, cambiar de directorio o quitarle blancos antes de abrirlo; toda condicion que deje de
leer como ruta una parte del literal hay que medirla contra esas tres familias, y ninguna medida
aqui las cerro todas. El contexto S1 del revisor tambien cuenta: con un solo tramo detras de `//`,
stable/F38z ya deja pasar `'// knowledge'[3:]`.

## Lo que se hizo con los hallazgos de la segunda pasada del revisor

Eje (a): 0 bloquea, 1 importa, 2 menor. Eje (b): 1 bloquea, 1 importa, 3 menor.

- **B-1 (bloquea, por medir): medido y confirmado** (R1-R4, arriba): F1 aplazado, como manda el
  punto 4 de la respuesta a la PARADA 2.
- **B-2 (importa): resuelto con el aplazamiento.** El comentario de `guardia.py` que afirmaba de
  mas sale con F1; el recuadro de `GUARDIAS-CLAUDE.md` se reescribio (ya no dice que solo queda el
  recorte a mitad de nombre).
- **B-3 (menor): hecho**: «Cada caso, estado final», abajo.
- **B-4 (menor): hecho**: la tabla de `make check` llega hasta `5f757439`; el del ultimo commit, en
  el mensaje de entrega.
- **B-5 (menor): cierto, se tiene en cuenta.** Las inserciones de esta rama buscan el ULTIMO
  «## Estado» y conservan lo que va detras (el guion de la sesion se cambio para eso tras la
  PARADA 2); el informe del revisor pegado no lleva ningun «## Estado».
- **A1 (importa): hecho.** Fila del 2026-11-13 en `HOLDOUT-EXPOSICIONES.md`, escrita tarde y dicho
  asi en la propia fila: los `make check` de `32316acf`, `55d41a02` y `5f757439` corrieron antes.
- **A2 (menor): hecho.** El recuadro de `GUARDIAS-CLAUDE.md` lleva las dos fechas.
- **A3 (menor): hecho.** La cabecera de `medida_parada2.py` dice que corrio una vez como test
  temporal y queda como anexo, y nombra el codigo muerto y la diferencia de `recursivo`.

## Cada caso, estado final

`F38z`, la guardia de stable/F38z-capa-generada; `rama`, la del ultimo commit. «W» solo Windows;
«W+L» los dos. Tests en `tests/unit/test_guardia_falsos_positivos.py` salvo que se diga.

| caso | test | F38z | rama | sistema |
|---|---|---|---|---|
| F2: `cmp` y `cmp -s` de dos ficheros nuevos de `docs/`, y el nombre con `=` de G.6 | `test_f2_cmp_de_dos_ficheros_que_no_son_guiones_pasa` | niega (ejecutar) | **pasa** | W+L |
| cmp con un protegido (2.º, 1.º, absoluto) y `diff` con uno | `test_f2_cmp_con_un_fichero_protegido_se_niega_por_la_lectura` | niega (`R_EJECUCION`) | niega (`R_HOLDOUT`) | W+L |
| B3: `cmp` como `diff` en las composiciones de C | `test_b3_cmp_como_diff_en_las_composiciones` | — | igual que `diff` | W+L |
| ROTO: sin `cmp` en `NO_EJECUTAN`; `cmp` sin leer sus argumentos | `test_roto_sin_cmp_en_no_ejecutan`, `test_roto_cmp_sin_leer_sus_argumentos` | — | cada uno rompe su test | W+L |
| F1: la copia de `generar_capa.py`, :364, :359, tabulador, `\\ `, D6 | `test_f1_*` (`xfail` estricto: «F1, aplazado») | niega | niega | W |
| h1, h1c, h2, h4-h8 | `test_h_los_casos_de_windows_siguen_negados` | niega | niega | W |
| h3 | `test_h3_el_punto_punto_sigue_negado` | niega | niega | W+L |
| B1 (blanco o tabulador detras del nombre) y B2 (oculto sin fragmento, con `/` y `\`; carpeta con el holdout, recortada y recorrida) | `test_revisor_las_variantes_siguen_negadas` y su gemelo contra la referencia | niega | niega | W |
| R1-R4 | `test_r_siguen_negados` y `test_r_la_referencia_niega` | niega | niega | W |
| D3: `//host/share/...`, `\\host\share\...`; un guion nuevo que nombra o recorre lo protegido | `test_d3_*` | niega | niega | W / W+L |
| D3: los de `test_guardia_alias.py` y `file://` de `test_guardia_g1.py` | esos tests, sin cambiar | niega | niega | W (y los de dos sistemas) |
| `//\| docs/x \|` y la f-cadena calculable | `test_lo_que_d1d_no_cubre_sigue_negado` | niega | niega | W |
| h1b `'x' + oculto[1:]` (limite conocido) y el recorte a mitad de nombre | `test_el_residuo_de_f1_es_la_clase_de_h1b` (mide e imprime; asegura que h1b pasa con las dos) | h1b pasa; el otro niega | h1b pasa; el otro niega | W |
| la referencia: F1 por no canonizar, F2 por ejecutar | `test_la_referencia_niega_f1_por_no_canonizar`, `..._f2_por_ejecutar` | — | — | W / W+L |
| la comparacion caso a caso (`medir_g1.py`, `i1`-`i3`) | `test_guardia_g1.py::test_la_comparacion_caso_a_caso_con_la_guardia_de_main` | — | `i2` declarado; `i1` e `i3` niegan en las dos | W+L |

Medido en la laptop tras aplazar F1: `test_guardia_falsos_positivos.py`, 48 passed y 6 xfailed; la
comparacion caso a caso de `test_guardia_g1.py`, en verde con solo `i2` declarado.

## El ensayo del cierre (D7), hecho (2026-11-13)

Sobre el ultimo commit de la rama, `82b19680`, en un clon independiente (`git clone`, no
`git worktree`), con la tabla de «El ensayo del cierre (D7), preparado para Aleks» y el paso 5 en la
rama (orden de cierre, punto 1b). El dia es el 2026-11-13: la fila de ese dia en
`HOLDOUT-EXPOSICIONES.md` cubre este `make check` (punto 1a: no hizo falta otra fila).

| # | Orden, como se lanzo | Quien | Salida |
|---|---|---|---|
| 1 | `git clone "C:/Users/USER/Desktop/Bot v3" C:/cm/gfpc` | Aleks, «!» | «done», 2543 ficheros |
| 2 | `git -C C:/cm/gfpc switch trabajo/guardia-falsos-positivos`; `git -C C:/cm/gfpc switch main` | sesion | la rama en `82b19680`; `main` en `4ecd7f17` |
| 3 | `git -C C:/cm/gfpc remote remove origin` | Aleks, «!» | sin salida (sin remoto) |
| 4 | `git -C C:/cm/gfpc config user.name ensayo`; `git -C C:/cm/gfpc config user.email ensayo@ejemplo.invalid` | Aleks, «!» | sin salida |
| 5 | `git -C C:/cm/gfpc switch trabajo/guardia-falsos-positivos`; `git -C C:/cm/gfpc rm -q contrato.yaml`; `git -C C:/cm/gfpc commit -q -m "chore(cierre): ensayo, sale el contrato"` | sesion | `4f7eecb0` |
| 6 | `git -C C:/cm/gfpc switch main`; `git -C C:/cm/gfpc merge --no-ff -q -m "merge: ensayo trabajo/guardia-falsos-positivos" trabajo/guardia-falsos-positivos` | sesion | merge `3acdacc7` |
| 7 | `git -C C:/cm/gfpc tag -a stable/F39a-guardia-falsos-positivos -m "ensayo"` | sesion | el tag del clon, sobre `3acdacc7` |
| 8 | `PROJECT_STATE.md` del clon: Current Branch `main`, Current Feature «Ninguna rama abierta...», Stable Main State y Last Stable Commit en `3acdacc7`; `git -C C:/cm/gfpc add PROJECT_STATE.md` | sesion | `M  PROJECT_STATE.md` y nada mas |
| 9 | `cd C:/cm/gfpc && make check > C:/cm/make-check-merge.log 2>&1; echo "exit=$?"` | Aleks, «!» | **exit=0** |
| 10 | leer el log | sesion | abajo; el clon lo borra Aleks con «!» |

Del log (`C:/cm/make-check-merge.log`):

```
CONTRATO: sin contrato.yaml: nada que comprobar
All checks passed!
3501 passed, 12 skipped, 6 xfailed in 1104.19s (0:18:24)
OK: rama 'main' - funcionalidad actual: Ninguna rama abierta. trabajo/guardia-falsos-positivos cerrada en main (ensayo, ...
SELLO: make check en verde sobre el arbol 0fcf5a10bebd89955210e01bf13880b1541bda85
PICO DE MEMORIA de make check: 277 MiB en `types` (suma de sus procesos, memoria comprometida, Windows; el mayor proceso, 267 MiB)
```

Ningun `failed` (`grep -c ' failed'` = 0). **Los 12 saltados, uno por uno** (lineas 100-108 del
log, el resumen `-rs`): 4 de `test_cuenta_7_de_agosto.py` y uno de `test_huecos_motor.py`,
`test_fidelidad_marzo.py`, `test_preparar_a35.py`, `test_selector_orden_stop.py`,
`test_simulacion.py` y `test_visor.py` (sin las velas o el dataset en el clon), uno de
`test_motor_prompt.py` (sin `tokenizers`) y uno de `test_contrato_rama.py` (sin `contrato.yaml`).
**Ninguno es de `test_guardia_g1.py` ni de `test_guardia_falsos_positivos.py`**: sobre el arbol
fusionado, `test_la_referencia_es_un_tag_y_no_es_esta_guardia` y
`test_la_comparacion_caso_a_caso_con_la_guardia_de_main` pasaron (no estan entre los saltados ni
hay ningun fallo). Los **6 xfailed** son los seis de F1 de `test_guardia_falsos_positivos.py` (en
`main` no habia ningun xfail: su `make check`, «3465 passed», sin xfailed). El ensayo, en verde.

**Correccion de la frase del paso 10** de la tabla preparada: decia «sin contrato no hay SELLO de
rama que exigir». No es asi: `make check` sella igual sin contrato (lo muestra la linea `SELLO`
de arriba); lo que no hay en el clon es quien exija el sello, porque un clon nuevo no trae los
hooks de `.git/hooks`.

### Lo que este ensayo no cubre

Como en GUARDIA-G1.md §13.7:

- **`pre-merge-commit`**: un clon nuevo no trae hooks (`.git/hooks` no se clona), asi que ni el
  commit del paso 5 ni el merge del paso 6 pasaron por la exigencia del sello. En el cierre real si
  pasan, y por eso el ritual sella antes de cada uno.
- **El contenido del commit del contrato**: el paso 5 solo saca `contrato.yaml`. El
  `chore(cierre)` real lleva ademas el registro en HISTORIA, la linea de Technical Debt, el estado
  de G.6 en la hoja de ruta y la fila de ERRORES-RECURRENTES (orden de cierre, punto 3); eso lo
  comprueba el `make check` del cierre real, no este.
- **El push y la CI de `main`**: el clon no tiene remoto.

## Estado

**F2 y G.6 entran; F1 se aplaza** (respuesta a la PARADA 2, punto 4: la segunda pasada del revisor lo
rompio con R1-R4, medidos). El diff de `guardia.py` contra stable/F38z es la entrada de `cmp`.

| commit | que |
|---|---|
| `6a310dc8` | apertura: encargo, contrato, Archivo 69 |
| `dce4004e` | fase 0 medida y PARADA |
| `f9888a03` | F1 (D1d) y F2, la referencia a F38z, los tests rotos contra F38z |
| `32316acf` | el informe: casos, encargo, cierre, ensayo, CI |
| `55d41a02` | la primera pasada del revisor (B1, B2) y la PARADA 2 |
| `5f757439` | la respuesta a la PARADA 2 (B1 con `strip`, B2 con los sufijos) |
| `82b19680` | F1 aplazado; la segunda pasada del revisor; A1-A3 y B-1..B-5 contestados |
| el ultimo | el ensayo del cierre y la orden de cierre (punto 1c) |

CI de `fix/guardia-falsos-positivos`: 43366719378 (`f9888a03`), 43379762621 (`5f757439`) y
43386236034 (`82b19680`), los tres con solo el fallo aceptado; la del ultimo commit, en el mensaje.
Revisor: dos pasadas enteras (opus), pegadas abajo; la primera, 2 bloquea (B1, B2: arreglados y
despues retirados con F1), 3 importa y 2 menor; la segunda, 1 bloquea (B-1: F1 roto, aplazado), 2
importa y 5 menor, todos contestados. El ensayo del cierre (D7), hecho y en verde sobre `82b19680`
(merge del clon `3acdacc7`, SELLO `0fcf5a10`). Esperando a que Aleks escriba `/cerrar-rama`.

Rama lista para revisión, NO cerrada.

## Anexo · El informe del revisor (primera pasada), pegado tal cual

## Informe del revisor · trabajo/guardia-falsos-positivos · 2026-11-13

HEAD 32316acf, base 4ecd7f17 (main = commit de estado de stable/F38z-capa-generada, 7bccf310). `git status --short` vacío.

**Resumen: la rama no está lista.** Hay dos bloqueos, y los dos son variantes de casos de D3 / h1-h8 que la guardia de stable/F38z niega y la de la rama deja pasar. El punto 6 de la respuesta del consultor dice que eso es motivo de parada.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 0 importa, 0 menor.

Sin hallazgos. Lo comprobado:
1. **Contrato.**
   - `uv run python scripts/contrato_rama.py` → «CONTRATO: 13 ficheros dentro del contrato de trabajo/guardia-falsos-positivos (riesgo medio, …, 4 comprobaciones para el revisor)», exit 0.
   - `uv run botsito state check` → OK, exit 0.
   - El pytest de las 5 guardias del contrato → exit 0, sin F ni E.
   - `make check` no lo ejecuté (escribe). Evidencia de `make-check.log`: «SELLO: make check en verde sobre el arbol a9a587ba…», que es igual a `git rev-parse HEAD^{tree}`; «3498 passed»; «PICO DE MEMORIA … 317 MiB».
2. **Trailers `Fuente:`.** Ningún commit toca `knowledge/spec` ni `knowledge/cases` (`git log main..HEAD -- knowledge/spec knowledge/cases` sale vacío).
3. **Holdout y material.** Nada bajo `knowledge/`. La fila del 2026-11-12 está en `HOLDOUT-EXPOSICIONES.md` (+1 línea). Los anexos no traen ninguna ruta protegida entera (grep de `cases/hol`, `transcripciones`, `caso-…`, `Users` sin resultados).
4. **Regímenes de cambio.** `git diff --name-status main...HEAD -- knowledge data/manifests` sale vacío. HISTORIA: 174 líneas añadidas, 0 borradas.
5. **Ambigüedades.** No se tocan.
6. **ADR.** Ninguno nuevo ni cambiado.
7. **Informes cerrados.** `GUARDIAS-CLAUDE.md` solo recibe 7 líneas añadidas, en un recuadro `>` con fecha y rama, junto a §1.7. El cuerpo queda intacto.
8. **Las tres guardias de una `cita`.** No aplica: ningún sitio nuevo con `cita`.
9. **Lo demás de `CLAUDE.md`.**
   - Ninguna cifra en la spec.
   - El informe existe y acaba en `## Estado`.
   - No hubo ensayos sobre copias sueltas.
   - Comprobé cinco citas contra su fuente, y las cinco cuadran:
     - `generar_capa.py:359` y `:364`, los dos literales tal cual;
     - `ACTIVAR-SESION-06-MOTOR.md:217-218`, el `cmp` negado con `diaria.DIAGNOSTICO.cuenta=diaria.txt`;
     - `CAPA-GENERADA.md:474`, «`cmp`, negado», en «La guardia» (:466);
     - `PROJECT_STATE.md:84` y `:152`, las dos líneas de deuda;
     - la regla de `NO_EJECUTAN` («La lista solo crece…»), en `guardia.py` de main hacia :2880.
10. **Items de evidencia nuevos.** Ninguno.

### Eje (b) · Encargo
Resumen: 2 bloquea, 3 importa, 2 menor. Requisitos: 21 hechos, 2 hechos de otra forma, 4 parciales, 0 no hechos, más el revisor (en curso).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Apertura: base, CI de main, ninguna otra rama | Hecho | informe :9-22 |
| 2 | Contrato con `tramo`, permitidas y protegidas | Hecho | `contrato.yaml:4-30` |
| 3 | Informe y anexos en sus rutas | Hecho | diff --name-status |
| 4 | F1: la copia cambiada de `generar_capa.py` pasa | Hecho | `test_f1_*` en verde (33 passed, ninguno saltado, Windows) |
| 5 | F2: `cmp` de dos ficheros pasa; `diff` comprobado; G.6 se cierra | Hecho | informe §c; `test_f2_*` |
| 6 | Lo que queda fuera (compilar.py, F38w, worktree add, lectores, D), con los lectores nombrados | Hecho | informe «Los demás lectores», «Líneas para el cierre» |
| 7 | D1d en `analizar_codigo`, sin tocar `_sin_prefijos`, `_canonica` ni `_absoluta` | Hecho | `git diff stable/F38z-capa-generada HEAD -- .claude/hooks/guardia.py` da 40 inserciones en tres trozos (:2892-2895, :4951-4952, :4986-5018). `_absoluta` :1298, `_no_canonizable` :1330, `_sin_prefijos` :1339 y `_canonica` :1365 no aparecen en el diff |
| 8 | D2: `cmp` en `NO_EJECUTAN` con su porqué; con un fichero protegido sigue negado | Hecho, con efectos no declarados (B3) | `guardia.py:2892-2895`; test :262-272 |
| 9 | D3: ningún caso que hoy se niega deja de negarse | **Parcial** | B1 y B2 |
| 10 | D4: en memoria, repo sintético, rutas a trozos, W o L por caso | Hecho | test :86-135; tabla de casos del informe |
| 11 | D5: la referencia sube a F38z; CAMBIOS_DECLARADOS = i1 e i2; casos i1-i3; el test roto pasa a i2 | Hecho | `test_guardia_g1.py:916`; `medir_g1.py:58-63`, :244-249, :365-368; `test_guardia_g1.py:1031` |
| 12 | D6: tests de F1 solo en Windows; no tarda | Hecho | test :202-225 (0,14 s según el informe) |
| 13 | D7: ensayo del cierre en un clon | Hecho de otra forma | la guardia niega `git clone`; queda preparado. Lo permite el punto 7 de la respuesta |
| 14 | Lo que NO cambia | Hecho | solo 13 ficheros, ninguno de src/, knowledge/, mql5/, settings, skills, agents, solo_lectura, Makefile ni .gitattributes |
| 15 | PROJECT_STATE: solo el ritual y «Tests Currently Passing»; tamaño | Hecho | diff de PS; `wc -c` da 24569; 2039→2058, que son las 19 funciones nuevas |
| 16 | Fase 0 a-f y PARADA | Hecho | informe :37-306 |
| 17 | La respuesta, copiada tal cual en el informe y en el encargo | Hecho | `diff` de encargo:68-80 contra informe:312-324 → IGUALES; el encargo solo crece desde 6a310dc8 |
| 18 | Tests primero, rotos contra F38z por su motivo | **Parcial** | B4 |
| 19 | h1b en el informe y en el recuadro de `GUARDIAS-CLAUDE.md` | Hecho | `GUARDIAS-CLAUDE.md` §1.7 |
| 20 | h1-h8, cada uno con test y su columna W/L | Hecho (pero ver B1 y B2) | test :276-315 |
| 21 | El residuo declarado (respuesta, punto 2) | Hecho | test :339-351 |
| 22 | `medir_windows.py` no se lanza y sale del repo | Hecho | `D` en f9888a03 |
| 23 | Líneas para el cierre (G.6, Technical Debt, tamaño, ERRORES) | Hecho (simuladas) | informe :474-494 |
| 24 | make check sellado en cada commit | Hecho | informe :532-538; el log da el sello de HEAD |
| 25 | Push a fix/ con su CI | **Parcial** | B5 |
| 26 | Revisor | En curso | este informe |
| 27 | Estado final y frase de cierre | **Parcial** | informe :542, «EN CURSO» (lo esperable antes de pegar el revisor) |
| 28 | Tabla «El encargo, punto por punto» | Hecho de otra forma | B6 |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| B1 | **bloquea** | **La condición 2 de D1d se salta con un blanco DETRÁS del nombre de máquina.** Los casos h4-h8 con un blanco a cada lado del nombre (p. ej. `\\ localhost \C$\<raíz>`, recorrida como h7 o con `os.stat` como h8) los niega F38z por no canonizar. En la rama, F1 se los salta. `_tramo_lleva_blanco` solo quita los blancos del principio: el tramo `" localhost "` queda en `"localhost "`, lleva blanco y devuelve True. La raíz real no lleva ningún fragmento de SENSIBLES, así que la condición 3 tampoco para el caso. El resultado es el mismo que mide el test roto a propósito sin la condición del blanco: h7 y h8 pasan. Que eso abra el repo de verdad depende de cómo resuelve Windows un servidor `" localhost "`. Es justo lo que habría medido `medir_windows.py`, y el punto 3 de la respuesta lo dio por innecesario en la premisa, ahora falsa, de que D1d niega toda esa familia. | `guardia.py:5002-5006` (`.lstrip(" \t")` y después `re.search(r"[ \t]", tramo)`). Test `_unc` :173-177: el blanco solo va delante del equipo. Test :414-421 (sin la condición del blanco, h7 y h8 pasan). Anexo `rotos-contra-F38z-SALIDA.txt:11` (F38z niega `// a b/…` por «no se puede canonizar», no por el fragmento) |
| B2 | **bloquea** | **La condición 3 (SENSIBLES) no cubre el material protegido que no lleva fragmento.** Es la variante de h1c: `"// a b/<fichero>"[7:]`, con un fichero de la lista `ficheros_con_ocultos.txt`. F38z la niega (no canoniza). La rama se salta el literal, y el recorte se hace al ejecutarse, así que lee el fichero. Un subíndice no es una composición de C. De las 14 rutas de esa lista, 13 no llevan ningún fragmento. El comentario de `guardia.py` afirma más de lo que el código sostiene: dice «un `"// <ruta protegida>"[3:]` se sigue mirando», y eso solo vale si la ruta lleva fragmento. Es la misma clase que h1b (`'x'+ruta[1:]`, que ya pasa en F38z), pero h1b se aceptó precisamente porque «ya pasa hoy con cualquier variante», y esta variante hoy NO pasa. Que entre o no en el límite de h1b lo decide el consultor. | `guardia.py:4996-4997` (el comentario) y :5014 (`not any(s in lit.lower() for s in SENSIBLES)`). `grep -v '^#' .claude/hooks/ficheros_con_ocultos.txt \| grep -ivc '<los 11 fragmentos>'` → **13**. `_es_composicion` :4392-4419 (Call, BinOp o JoinedStr; no Subscript). Medida indirecta: la propia guardia de la rama, ante mi `python -c` con la lista `['// a b/knowledge/_proposals/x.yaml', '// a b/docs/validation/anexos/X/y-SALIDA.txt', '// a b/docs/caso-…md', '// a b/knowledge/feedback/x.yaml', …]`, solo negó el cuarto, el que lleva fragmento. Los tres primeros van antes en `ast.walk` y sin F1 los habría negado por no canonizar. No lo medí de punta a punta con `decidir` |
| B3 | importa | **`cmp` en `NO_EJECUTAN` tiene dos efectos más que el informe no declara.** El informe dice «No hace falta más» (§d) y el comentario de `NO_EJECUTAN` solo dice que sus argumentos se miran como una lectura. (1) `_empieza_por_un_programa`: una f-cadena o una suma que empieza por `cmp ` deja de ser una composición de C. Medido en memoria: `f"cmp {a}/b/c"` y `"cmp " + a + "/b/c"` dan **True sin `cmp` y False con `cmp`**, igual que `diff`; `xxd` sigue en True. (2) `cmp` entra en `PROGRAMAS_DE_DATOS`: la regla de la CI deja de mirar sus argumentos. Esto no tiene riesgo, porque `cmp` no ejecuta nada. Sin cambios: `BUILTINS_NO_ADMITIDOS`, porque `cmp` no está en `BUILTINS_SHELL`, y `PS_NO_EJECUTAN`, donde no está. El efecto (1) es el mismo trato que ya tiene `diff`, pero ningún test lo fija y el informe no lo dice. | `guardia.py:4422-4444` (`prog in NO_EJECUTAN`), :5071, :3307-3313. Mi `python -c` sobre `_es_composicion` (salida citada). Quise medir la consecuencia con una ruta protegida a trozos y la guardia lo negó; ver «Lo que no pude comprobar» |
| B4 | importa | **El anexo de los tests rotos no incluye `test_f1_el_literal_no_llega_a_absoluta_ni_tarda`.** La tabla del informe le pone «niega» con F38z (:407) y el informe habla de «15 fallos». El anexo trae 15 FAILED y este test no está entre ellos. Por lógica tiene que fallar, porque usa la misma entrada que `test_la_referencia_niega_f1_por_no_canonizar`, pero la evidencia citada no lo muestra. | `rotos-contra-F38z-SALIDA.txt:16-30`; informe :361 y :407; test :201-225 |
| B5 | importa | **La CI de fix/ no es del último commit.** `origin/fix/guardia-falsos-positivos` está en f9888a03 y HEAD en 32316acf. La skill `entregar-rama` dice que el run que cuenta es el del último commit (pasos 7 y 9, y su verificación). | `git rev-parse refs/remotes/origin/fix/guardia-falsos-positivos` → f9888a03…; informe :523 |
| B6 | menor | La tabla se llama «El encargo frente a lo hecho», no «El encargo, punto por punto». Tampoco parte cada punto de la respuesta con los cuatro estados. El nombre lo usa el propio encargo (punto 7), así que no es grave. | informe :446-464; `entregar-rama/SKILL.md:50,97` |
| B7 | menor | **La fixture `base`** es correcta y no enmascara nada: hace que h7 y h8 dependan de la condición del blanco y no del fragmento `data\` de `AppData\`, que es lo que necesita `test_roto_sin_la_clausula_del_blanco`. Además se asegura de que la carpeta nueva no lleve ningún fragmento y comprueba el borrado. Dos pegas de forma: escribe fuera del temporal de pytest, en la carpeta del usuario, y si el proceso muere de golpe (el recorte por memoria que nombra `CLAUDE.md`) deja `gfp-*` allí, como ya pasó 130 veces. Hoy no queda ninguna. | test :86-112; `ls -d /c/Users/USER/gfp-*` → 0; informe :386-392 |

Sobre los puntos del alcance que me pasaste:
- **(1) Comparación caso a caso con F38z.** El diff es exactamente el bloque F1, la línea del bucle y la entrada de `cmp`. Efectos además de esos: B3. Que F1 se salte un literal tiene otro efecto: no suma a `directorios`, con lo que la regla de :4969 se dispara más, nunca menos. En esa dirección no abre nada.
- **(2) D3 y h1-h8.** Todos sus tests niegan en la rama: 33 passed sin saltados, y `test_guardia_alias.py` y `test_guardia_g1.py` en verde. Pero hay variantes sin test que pasan: B1 y B2.
- **(3) Los tests contra F38z.** El anexo muestra cada fallo con su motivo, salvo B4. Los dos tests de la suite que cargan la guardia del tag pasan (corrieron: no saltaron).
- **(4) `_sin_prefijos`, `_canonica` y `_absoluta`** están intactas.
- **(5) D5:** correcto. En Linux i1 queda declarado aunque no difiere, y es inocuo: `medir_g1.main` solo falla por lo que difiere sin declarar (:438-443).
- **(6) La fixture:** ver B7.

### Lo que no pude comprobar
- **B1 y B2 de punta a punta, con `decidir`.** Necesitan un repo sintético en disco, y yo no escribo. Además la guardia me negó las medidas en memoria que montaban una ruta protegida a trozos («el codigo compone knowledge/cases/holdout/1/x.yaml») y las que cargaban la guardia del tag con `exec` («el codigo carga o ejecuta `exec(...)`»). No las reescribí. Para confirmarlos, la sesión puede añadir tests:
  - B1: `_unc(repo, " ", "localhost ")` con el caso de h7 o de h8, que debería negarse;
  - B2: un `docs/oculto.txt` listado en `.claude/hooks/ficheros_con_ocultos.txt` del repo sintético, con `print(open("// a b/docs/oculto.txt"[7:]).read())`, que debería negarse.
  Los dos los niega F38z.
- **Si Windows resuelve un servidor con blancos (`" localhost "`).** `medir_windows.py` no se lanzó, por el punto 3 de la respuesta.
- **El efecto de B3 sobre una composición con una ruta protegida.** La guardia lo negó, como en el primer punto.
- **La suite nueva entera contra la guardia de F38z.** Haría falta cargar el tag con `exec`, que la guardia niega. Me baso en el anexo y en los dos tests de referencia.
- **`make check` y la CI.** No los ejecuté: `make check` escribe, y la CI la comprobé solo por la referencia de `fix/`. Evidencia: `make-check.log` y el informe (:520-538).

### Comandos ejecutados
1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
2. `git diff main...HEAD -- .claude/hooks/guardia.py && git diff stable/F38z-capa-generada HEAD --stat -- .claude/hooks/guardia.py && git rev-parse stable/F38z-capa-generada^{commit} main`
3. Grep `NO_EJECUTAN|PROGRAMAS_DE_DATOS|BUILTINS_NO_ADMITIDOS`, `_es_composicion`, `SENSIBLES`, `ficheros_con_ocultos`, y Read de varios tramos de `guardia.py`
4. `uv run python scripts/contrato_rama.py`
5. `uv run pytest tests/unit/test_guardia_falsos_positivos.py -q -p no:cacheprovider -rs` (33 passed) y la misma con `-v`
6. `ls -d /c/Users/USER/gfp-* | wc -l` → 0
7. `uv run pytest tests/unit/test_guardia_g1.py tests/unit/test_guardia_claude.py tests/unit/test_guardia_alias.py tests/unit/test_guardia_ci.py tests/unit/test_guardia_ffmpeg.py -q -p no:cacheprovider` → exit 0
8. `git diff main...HEAD -- tests/unit/test_guardia_g1.py docs/validation/anexos/GUARDIA-G1/medir_g1.py docs/validation/GUARDIAS-CLAUDE.md docs/validation/HOLDOUT-EXPOSICIONES.md PROJECT_STATE.md`
9. `git diff --name-status main...HEAD` (y las variantes sobre `knowledge`, `data/manifests` y `docs/adr`); `git diff main...HEAD --numstat`; `git log --name-status main..HEAD`
10. `tail` y `grep SELLO|PICO|passed|failed make-check.log`; `git rev-parse HEAD^{tree}`
11. `grep -n` de los dos literales en `generar_capa.py`; `git show main:.claude/hooks/guardia.py | sed -n '2876,2892p'`; `sed -n '214,222p' docs/validation/ACTIVAR-SESION-06-MOTOR.md`; Grep `cmp` en `CAPA-GENERADA.md`
12. `uv run python -c` (comparación con el tag por `exec`) → **NEGADO** por la guardia; no lo reescribí
13. `uv run python -c` sobre `_es_composicion` con la guardia de la rama por ruta literal (sin `cmp` y con `cmp`)
14. `uv run python -c` con `analizar_codigo` sobre una ruta protegida a trozos → **NEGADO**; no lo reescribí
15. `uv run botsito state check`
16. `wc -c PROJECT_STATE.md`; `git show main:PROJECT_STATE.md | wc -c`; `sed -n '84p;152p' PROJECT_STATE.md`; `grep -n G.6 docs/plan/HOJA-DE-RUTA.md`
17. `grep -c` y `grep -n -i` sobre los anexos
18. `diff` de la respuesta en el encargo contra la del informe → IGUALES; `git diff 6a310dc8 HEAD -- docs/encargos/…` → 0 líneas borradas
19. Read de `.claude/skills/entregar-rama/SKILL.md`
20. `git branch -r`; `git rev-parse --verify -q refs/remotes/origin/fix/guardia-falsos-positivos`
21. `grep -n requires-python pyproject.toml`; `cat .python-version`
22. `wc -l` y `cut | sort | uniq -c` de `.claude/hooks/ficheros_con_ocultos.txt`; recuento de las rutas sin fragmento → 13
23. `uv run python -c` sobre `_comentario_que_no_es_ruta` con cinco literales sintéticos → **NEGADO** en el cuarto (con fragmento); no lo reescribí. La negativa sirve de medida indirecta en B2

Ficheros: C:\Users\USER\Desktop\Bot v3\.claude\hooks\guardia.py, C:\Users\USER\Desktop\Bot v3\tests\unit\test_guardia_falsos_positivos.py, C:\Users\USER\Desktop\Bot v3\docs\validation\GUARDIA-FALSOS-POSITIVOS.md, C:\Users\USER\Desktop\Bot v3\docs\validation\anexos\GUARDIA-FALSOS-POSITIVOS\rotos-contra-F38z-SALIDA.txt, C:\Users\USER\Desktop\Bot v3\docs\validation\anexos\GUARDIA-G1\medir_g1.py, C:\Users\USER\Desktop\Bot v3\tests\unit\test_guardia_g1.py, C:\Users\USER\Desktop\Bot v3\.claude\hooks\ficheros_con_ocultos.txt

## Anexo · El informe del revisor (segunda pasada, entera), pegado tal cual

## Informe del revisor · trabajo/guardia-falsos-positivos · 2026-11-13

HEAD 5f757439, base 4ecd7f17 (main, el commit de estado de stable/F38z-capa-generada, 7bccf310). `git status --short` vacío. `origin/fix/guardia-falsos-positivos` apunta a 5f757439.

**Resumen.** El eje (a) está limpio salvo la fila de exposiciones del 13. El alcance nuevo sí da resultado: encuentro **tres formas que, según el código, la guardia de stable/F38z niega y la de la rama deja pasar**, sin recortar a mitad de un nombre (R1, R2 y R3). Hay una cuarta, R4, que encaja en la plantilla del residuo declarado pero no recorta a mitad de un nombre. **Ninguna está medida de punta a punta** (por qué, en «Lo que no pude comprobar»). Las cuatro van como propuesta de test. Si la sesión las confirma, el punto 4 de la respuesta a la PARADA 2 saca F1 de la rama.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 1 importa, 2 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| A1 | importa | **No hay fila del 2026-11-13 en `HOLDOUT-EXPOSICIONES.md`, aunque ese día corrieron los `make check` de tres commits.** Cada uno lee el M1 de marzo, según la propia fila de la rama. ADR-0021 §4 dice «Toda exposicion se anota el mismo dia». La única fila de la rama es del 12 y habla de «los `make check` de la rama» en general. El precedente de `trabajo/laminas` es una fila por día, «declarado ANTES del primer `make check` del día». Si el consultor lee la fila del 12 como si cubriera toda la rama, el hallazgo es solo de forma. Si no, falta una fila, que se añade al final (el fichero solo crece). | `git log --date=iso`: 32316acf 2026-11-13 00:14, 55d41a02 01:01, 5f757439 01:35. `make-check.log`, de 2026-11-13 01:35, con SELLO del árbol de HEAD. `grep` de filas por fecha y rama: la última de esta rama es `2026-11-12`. `HOLDOUT-EXPOSICIONES.md:136` (laminas, 11-11). `docs/adr/0021-que-cuenta-como-abrir-un-holdout.md:26` |
| A2 | menor | El recuadro de `GUARDIAS-CLAUDE.md` §1.7 se amplió el 13 (ya cita la PARADA 2), pero sigue fechado «2026-11-12». | `git diff f9888a03 HEAD -- docs/validation/GUARDIAS-CLAUDE.md`: cinco líneas `+>` que nombran la «PARADA 2, punto 1»; el recuadro empieza por «CORRECCION (2026-11-12 …)» |
| A3 | menor | `medida_parada2.py` está commiteado, pero su docstring dice «Se borra antes de commitear». Además, la línea 43 es código muerto, porque la 44 la pisa. Y su variante «B1+b» mira las carpetas siempre en recursivo (`recursivo=True`), mientras que lo implementado usa `recursivo=recorre`. La tabla de la PARADA 2 mide entonces una variante algo distinta de la que entró. Lo implementado sí lo miden los tests de la suite. | `anexos/GUARDIA-FALSOS-POSITIVOS/medida_parada2.py:1-2, 43-44, 55`. `guardia.py:4988` |

Comprobado sin hallazgos:
1. **Contrato.**
   - `uv run python scripts/contrato_rama.py` da «CONTRATO: 15 ficheros dentro del contrato de trabajo/guardia-falsos-positivos (riesgo medio, …, 4 comprobaciones para el revisor)».
   - `uv run botsito state check` da OK.
   - El pytest de las cinco guardias del contrato sale con exit 0, todo en puntos.
   - `make check` no lo ejecuté (escribe). En `make-check.log`: «3516 passed», «SELLO: make check en verde sobre el arbol 0c5318da…», que es igual a `git rev-parse HEAD^{tree}`, y «PICO DE MEMORIA … 316 MiB».
2. **Trailers `Fuente:`.** No aplican: ningún commit toca `knowledge/spec` ni `knowledge/cases`.
3. **Holdout y material.** Nada bajo `knowledge/`, `data/` ni `corpus/`. Se ha medido en repos sintéticos.
4. **Regímenes de cambio.** El `--name-status` no toca `knowledge/evidence`, `knowledge/feedback`, `data/manifests` ni el corpus. Solo crecen: HISTORIA (174/0), `GUARDIAS-CLAUDE.md` (11/0) y `HOLDOUT-EXPOSICIONES.md` (1/0).
5. **Ambigüedades.** No se tocan.
6. **ADR.** Ninguno.
7. **Informe cerrado (`GUARDIAS-CLAUDE.md`).** Solo recibe un recuadro `>` con fecha y rama; el cuerpo queda intacto.
8. **Las tres guardias de una `cita`.** No aplica.
9. **Lo demás de `CLAUDE.md`.**
   - `PROJECT_STATE.md` pesa 24.569 bytes. Su diff solo toca Current Branch/Feature, la cifra de tests (2064) y el número de Archivo.
   - Las citas comprobadas cuadran:
     - `generar_capa.py:359` y `:364`, tal cual;
     - `guardia.py:2857` (`diff`), `:2880` («La lista solo crece…») y `:1076` (`sha1sum` en `LECTOR_DE_METADATOS`);
     - `ACTIVAR-SESION-06-MOTOR.md:217-218` (`cmp` negado sobre `diaria.DIAGNOSTICO.cuenta=diaria.txt`);
     - `HOJA-DE-RUTA.md:792` (G.6).
10. **Items de evidencia nuevos.** Ninguno.

### Eje (b) · Encargo (y las dos respuestas del consultor)
Resumen: 1 bloquea (por medir), 1 importa, 3 menor. Requisitos: 27 hechos, 2 hechos de otra forma, 4 parciales, 0 no hechos.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Apertura: base, origin, tag, CI de main, ninguna otra rama | Hecho | informe :9-22 |
| 2 | abrir-rama: encargo, contrato, Archivo 69 | Hecho | 6a310dc8; HISTORIA +174/-0 |
| 3 | Contrato: `tramo`, permitidas y protegidas del encargo | Hecho | `contrato.yaml:4-30` |
| 4 | Informe y anexos en sus rutas | Hecho | `--name-status` |
| 5 | F1: la copia de `generar_capa.py` pasa (:359 y :364) | Hecho | 51 passed y 0 saltados en Windows (`test_f1_*`) |
| 6 | F2: `cmp` de dos ficheros pasa; `diff` comprobado; G.6 se cierra | Hecho | `guardia.py:2892-2895`; informe §c |
| 7 | Lo que queda fuera (`/`, F38w, worktree add, lectores nombrados, `fc`, D) | Hecho | informe :441-447 y :477-489 |
| 8 | D1 como D1d, en negativo, solo en `analizar_codigo` | Hecho | diff: :4951-4957 y el bloque :4998-5042 |
| 9 | F1 no toca `_sin_prefijos`, `_canonica` ni `_absoluta` | Hecho | el diff no tiene hunks en :1298-1395. `_mirar_literal` es el cuerpo del bucle anterior sin cambios (comparado línea a línea) |
| 10 | D2: `cmp` en NO_EJECUTAN, con sus argumentos leídos y el protegido negado | Hecho | test :263-273, en verde |
| 11 | **D3: ningún caso que hoy se niega deja de negarse** | **Parcial, por medir** | B-1 |
| 12 | D4: en memoria, repo sintético, W o L por caso | Hecho | test :86-186; tabla :403-432 |
| 13 | D5: referencia F38z, lista vaciada, solo i1 e i2 | Hecho | `test_guardia_g1.py:916`; `medir_g1.py` (CAMBIOS_DECLARADOS = i1, i2); `test_roto_la_comparacion_con_main` borra `i2-f2-cmp` |
| 14 | D6: F1 solo en Windows y no tarda | Hecho | `SOLO_WINDOWS`; test :202-226 |
| 15 | D7: ensayo del cierre en un clon | Hecho de otra forma | la guardia niega `git clone`; las órdenes están en :499-521 (respuesta 1, punto 7) |
| 16 | Lo que NO cambia | Hecho | 15 ficheros, ninguno de src/, knowledge/, mql5/, settings, skills, agents, solo_lectura, Makefile ni .gitattributes |
| 17 | PROJECT_STATE: solo el ritual y los tests; tamaño medido | Hecho | diff de PS; `wc -c` da 24569 |
| 18 | Fase 0 a-f y PARADA | Hecho | informe :37-306 |
| 19 | Respuesta 1 (puntos 0-5) aplicada | Hecho | informe :326-355 |
| 20 | Respuesta 1, punto 3: `medir_windows.py` fuera | Hecho | no está en el árbol |
| 21 | Respuesta 1, punto 4: h1b en el informe y en el recuadro, no en Technical Debt | Hecho | recuadro de `GUARDIAS-CLAUDE.md` |
| 22 | Respuesta 2, punto 0 (B1: `strip`) | Hecho | `guardia.py:5022` |
| 23 | Respuesta 2, punto 1 (B2: sufijos; residuo declarado con medida contra F38z) | Hecho, pero ver B-1 | `guardia.py:4955-4956, 5026-5031`. Mi corrida imprime «F38z residuo NIEGA / rama residuo PASA / h1b PASA en las dos» |
| 24 | Respuesta 2, punto 2 (B3 con test) | Hecho | `test_b3_cmp_como_diff_en_las_composiciones` |
| 25 | Respuesta 2, punto 3 (los xfail pasan a tests normales; sello; push a fix/) | Hecho, salvo la CI | tests :335-372 sin xfail; origin/fix = 5f757439 |
| 26 | CI de fix/ del último commit (solo el fallo aceptado) | Parcial | en marcha según el contexto; el informe aún no trae el run |
| 27 | Respuesta 2, punto 4 (este revisor) | En curso | este informe |
| 28 | Respuesta 2, punto 5 (órdenes de D7 en el estado final) | Parcial | la tabla :505-516 existe; falta revalidarla en el estado final |
| 29 | Respuesta 2, punto 6 (Lista para revisión, commits, runs, revisor, F1 sí o no) | Parcial | `## Estado`: «EN CURSO» |
| 30 | Las respuestas, copiadas tal cual en el encargo y en el informe | Hecho | `diff` de encargo:68-80 contra informe:312-324 y de encargo:86-96 contra informe:618-628 → IGUALES las dos. El encargo solo crece (34/0 desde 6a310dc8) |
| 31 | «El encargo, punto por punto» | Hecho | informe :449-467 |
| 32 | make check sellado en cada commit | Hecho de otra forma | el log sella HEAD; la tabla del informe acaba en f9888a03 (ver B-4) |
| 33 | Comparación caso a caso con F38z (alcance de la primera pasada) | Hecho | el diff contra el tag es el bloque F1, `_mirar_literal` (extraída sin cambios) y la entrada de `cmp`. Los efectos de `cmp` ya están declarados (B3) |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| B-1 | **bloquea (por medir)** | **F1 deja pasar casos que stable/F38z niega y que no son un recorte a mitad de un nombre** (R1, R2 y R3, en la sección siguiente). La causa es una sola: **los sufijos de un literal de F1 se resuelven contra `ctx.cwd`**. Eso solo coincide con la ruta real cuando la cabeza no es una carpeta de verdad y la ruta no es absoluta.<br>(1) Si la cabeza es una carpeta real con blancos (`Bot v3`, `estrategia del trader`) y el directorio de trabajo no es la raíz (`cd ..`, `cd corpus`), quitar la marca `// ` (h1 o h2 tal cual) da una ruta que ningún sufijo nombra.<br>(2) Si la cola es una ruta absoluta por el recurso de administración de la propia máquina (`C$`), sus sufijos se miran como relativos, y solo la raíz o un ancestro escapan desde la raíz; desde otra carpeta escapa cualquier fichero. Por el punto 4 de la respuesta 2, si se confirma, F1 sale de la rama. | `guardia.py:4955-4956` (los sufijos a `_mirar_literal` con `ctx.cwd`), `:4980` (`_absoluta(ruta_texto, ctx.cwd)`), `:1699-1708` (`cd` cambia `ctx.cwd`), `:3936-3937` (`cd` se admite delante de una ejecución). Medido con la guardia del árbol: `_comentario_que_no_es_ruta('// Bot v3/knowledge')` da True con sufijos `['knowledge']`; `'// estrategia del trader/sesiones/x.txt'` da True con `['sesiones/x.txt', 'x.txt']` |
| B-2 | importa | **Dos textos afirman más de lo que el código sostiene, si se confirma B-1.**<br>El recuadro de `GUARDIAS-CLAUDE.md` dice que solo queda «recortado a MITAD de un nombre» y que «los recortes por un separador si se miran».<br>El comentario de `guardia.py` dice que «lo unico que se exime es la CABEZA».<br>R1 y R2 quitan justo la marca. R3 no recorta. R4 corta en la frontera de un nombre. | recuadro de `GUARDIAS-CLAUDE.md` §1.7; `guardia.py:5010-5015` |
| B-3 | menor | La tabla «Cada caso, con su test y sus dos decisiones» no recoge los casos de la PARADA 2 (b1-*, b2-*, el residuo medido); solo están en «Aplicación». | informe :403-432 frente a :630-666; test :311-395 |
| B-4 | menor | La tabla de `make check` acaba en f9888a03. Faltan 32316acf, 55d41a02 y 5f757439, aunque el log sella HEAD. | informe :535-541; `make-check.log` |
| B-5 | menor | Lo que el revisor anterior pegó lleva su propio `## Informe del revisor` de nivel 2 después de `## Estado`. Si alguien inserta texto buscando el último encabezado, caerá dentro del anexo. | informe :672-678 |

### Intentos de romper F1

Criterio, el tuyo: el caso cuenta si stable/F38z lo niega y la rama lo deja pasar. No cuentan ni el recorte a mitad de un nombre ni lo que ya pasa con stable/F38z con un literal normal de la misma ruta.

Las decisiones de F38z salen de `git show stable/F38z-capa-generada:.claude/hooks/guardia.py`: `_sin_prefijos`, `_canonica` y `_absoluta` son las mismas que en la rama. Las de la rama, de `guardia.py:4943-5042`. Todo «por medir» salvo lo que digo medido.

**Los que, por el código, cuentan:**

**R1. h1 con `cd` a una carpeta.** `cd corpus && uv run python -c "print(open('// estrategia del trader/sesiones/x.txt'[3:]).read())"` (vale igual `.lstrip('/ ')`).
- **F38z: NIEGA.** `_sin_prefijos` casa equipo « estrategia del trader», recurso «sesiones», y cae en `_no_canonizable`. El literal normal `'estrategia del trader/sesiones/x.txt'`, con `ctx.cwd`=corpus, da R_HOJA por `motivo_fichero:581`.
- **Rama: PASA.** El tramo «estrategia del trader» lleva blanco y no hay fragmento de SENSIBLES. Los sufijos `sesiones/x.txt` y `x.txt` resuelven a `corpus/sesiones/x.txt` y `corpus/x.txt`, que no son la zona.
- Al ejecutarse lee `corpus/estrategia del trader/sesiones/x.txt`, que es una hoja.
- Test propuesto: en el repo inventado, `_decide(g, repo, "cd corpus && uv run python -c \"…\"")`. R_HOJA es por ruta, así que no hace falta que el fichero exista.

**R2. h1 con `cd ..` (la cabeza es la carpeta del repo).** `cd .. && uv run python -c "import os; print([r for r,_,_ in os.walk('// Bot v3/knowledge'[3:])])"`.
- **F38z: NIEGA** (`_no_canonizable`: equipo « Bot v3», recurso «knowledge»). El literal normal `'Bot v3/knowledge'` con `ctx.cwd`=Escritorio recorre `repo/knowledge` y lo niega `motivo_directorio`.
- **Rama: PASA.** El único sufijo, `knowledge`, va al Escritorio, donde no existe. La regla de `recorre` no salta porque el código no lleva ningún fragmento de SENSIBLES.
- Al ejecutarse recorre `knowledge/` con el holdout. La variante de fichero es `'// Bot v3/docs/validation/anexos/<oculto>'[3:]`.
- Test propuesto: el repo inventado en una carpeta con blanco (`base / "r b"`), `cwd` = `base`, y `'// r b/knowledge'[3:]` con `rglob`.

**R3. h7 con un blanco DENTRO del nombre, quitado al ejecutarse.** Desde la raíz, sin `cd`:
```
Path('\\\\ local host\\C$\\Users\\USER\\Desktop\\Bot v3'.replace(' ', '', 2)).rglob('*')
```
- **F38z: NIEGA** (`_no_canonizable`). El literal normal `\\localhost\C$\<raíz>` lo canoniza a la raíz y lo niega por recorrerla: es h7.
- **Rama: PASA.** El tramo «local host» lleva blanco y no hay fragmento. Los sufijos `C$\Users\…\Bot v3`, …, `Bot v3` se miran como relativos a la raíz: ninguno existe.
- `.replace` no lo calcula C (`_calcular:4360-4389`).
- **R3b**, la misma idea con `cd docs` y un fichero sin fragmento (`…\Bot v3\knowledge\_proposals\<f>`): el sufijo `knowledge\_proposals\<f>` resuelve contra `docs/` y deja de verse.
- Test propuesto: `_recorre` sobre `_unc(repo, " ", "local host")` + `.replace(' ', '')` (la ruta del repo inventado no lleva blancos).

**Dentro de la plantilla declarada, pero sin recorte a mitad de un nombre:**

**R4.** `Path('// a b/x//localhost/C$/Users/USER/Desktop/Bot v3'[8:]).rglob('*')`, desde la raíz.
- **F38z: NIEGA** (equipo « a b», recurso «x»).
- **Rama: PASA.** Los sufijos son `x//localhost/…`, `/localhost/…` (relativa a la unidad: `C:\localhost\…`), `localhost/…`, …, `Bot v3`. Ninguno es `//localhost/…`, porque los sufijos empiezan DETRÁS de cada separador, nunca EN él.
- Es la plantilla `"// a b/x<ruta>"[8:]`, con `<ruta>` = `//localhost/C$/<raíz>`. El corte cae en la frontera de «x», no a mitad. Su gemelo h1b (`'x//localhost/…'[1:]`) pasa con F38z.
- Decide el consultor si es residuo.

**Contexto que pesa en la decisión (no son hallazgos de la rama):**
- **S1. Con UN solo tramo detrás de `//`, F38z ya deja pasar h1.** `_sin_prefijos:1356-1358` devuelve la ruta tal cual si no hay recurso. Así, `os.walk('// knowledge'[3:])` desde la raíz pasa con F38z y con la rama, porque «knowledge» solo no es fragmento. Y `cd .. && … os.walk('// Bot v3'[3:])` pasa con F38z.
- Es decir: lo que alcanzan R1 y R2, F38z ya lo alcanza con un hermano de un tramo. Y R3 y R4, con un disfraz de literal normal (`'C :/…'.replace(' ', '')`, o h1b).
- Por la letra de tu criterio, R1-R3 cuentan, porque F38z niega ese guion exacto y el literal normal de la misma ruta. En riesgo, no abren material que F38z no abriera ya por otra forma. Lo decide el consultor.
- Por el código, un arreglo que miraría R1 y R2 es mirar también la cabeza sin la marca, `lit[2:].lstrip(" \t")`, como un sufijo más. R3, R3b y R4 piden otra cosa: mirar como absolutos los sufijos que siguen a un recurso `C$` de la propia máquina. Ninguno de los dos está medido.

**Los que no rompen (razonados sobre el código):**
- El literal tal cual (`open('// a b/x')`): al ejecutarse es un recurso de red con blanco en el servidor, y no llega a nada local. Es F1 mismo.
- Recorte en un separador (`[k:]` tras `/` o `\`), con la raíz como directorio de trabajo: es un sufijo y se mira (B2).
- Separadores repetidos (`// a b//x`): F38z no niega, porque el recurso queda vacío y `_sin_prefijos:1356` no casa.
- Mezclas de `/` y `\`: el mismo regex, `[\\/]`.
- `..` en la cola: el sufijo tras el primer `..` es la misma ruta que se abre. `.` y `/.` cuando se recorre: el sufijo `.` es la raíz y se niega.
- `+`, `os.path.join`, `Path(a, b)`, `/` o `joinpath` con el literal de F1 al principio: C calcula el conjunto y `_exigir_ruta_del_codigo` lo niega por no canonizar, en las dos guardias.
- f-cadena con una variable calculable: niega en las dos (el residuo). Con una variable no calculable: el trozo constante sin recurso ya pasaba con F38z.
- `split()` o cortes dentro de la cabeza, tras un blanco: es la clase de h1b, porque el literal normal `'a knowledge/x'.split()[-1]` pasa con F38z.
- Lo que lleva SENSIBLES (holdout, corpus, transcripciones, `data/`, material adicional, backtest, xlsx, cruda, `knowledge/cases` o `knowledge/feedback`): la condición 3 lo saca de F1.
- `ficheros_con_ocultos.txt`: 14 entradas, 10 en `knowledge/_proposals` y 4 en `docs/validation`, ninguna en la raíz y ninguna con blancos (medido con `grep`/`cut`). Desde la raíz las cubre el sufijo; solo escapan con `cd` (R2, R3b).
- `file:`: se mira antes. Más de 400 caracteres o un salto de línea: se salta en las dos. Linux: la puerta `os.name`.

### Lo que no pude comprobar
- **R1-R4 y S1 de punta a punta con `decidir`.** Medirlos obliga a montar rutas protegidas a trozos (un `cwd` más una ruta relativa, o la raíz por `C$`) y a escribir un repo sintético en disco. No lo hice, por tu indicación y porque solo leo. Además, mi propio comando con `os.walk` y `'// Bot v3/knowledge'` lo negaría la guardia activa (el sufijo `knowledge` contra la raíz). Medí solo los predicados (salida arriba).
- **Si `\\localhost\C$` se abre desde un proceso sin elevar.** R3, R3b y R4 dependen de ello, igual que h4-h8, que son casos de D3. No se ha medido nunca, porque `medir_windows.py` no se lanzó.
- **Si Windows recorta blancos raros en un nombre de servidor.** Ejemplo: `// localhost \u00a0/C$/x` (blanco normal más uno no separable). Es F1 (medido: True), pero el blanco no separable no está en `strip(" \t")`.
- **Cuánto tarda `realpath` sobre `\\ <nombre>` sin recurso** (S1, con F38z): podría tocar la red, y el tope del hook es de 30 s.
- **La CI de 5f757439**: en marcha; no la consulté.
- **`make check`**: escribe. Evidencia: `make-check.log` (arriba).

### Comandos ejecutados
1. `git branch --show-current && git merge-base main HEAD && git rev-parse main stable/F38z-capa-generada^{commit} && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
2. `git diff main...HEAD -- .claude/hooks/guardia.py`
3. Read: encargo, `contrato.yaml`, el informe entero, `test_guardia_falsos_positivos.py`, `medida_parada2.py`, `parada2-windows-SALIDA.txt`, y los tramos de `guardia.py` 440-770, 1100-1144, 1200-1410, 1690-1714, 3925-3945, 4080-4189, 4240-4590, 4880-5057. Grep en `guardia.py`, `ADR-0021` y `generar_capa.py`.
4. `cd … && ls -a && cat .python-version && uv run python --version` → **NEGADO** (una ejecución detrás de `ls`). Lo partí como propone la guardia: `ls -a && cat .python-version`.
5. `grep -v '^#' .claude/hooks/ficheros_con_ocultos.txt | grep -c .` (14) y `| grep -vc /` (0); `| grep -c ' '` (0); `| cut -d/ -f1-2 | sort | uniq -c`
6. `uv run python scripts/contrato_rama.py`
7. `uv run botsito state check`
8. `uv run pytest` de los cinco ficheros del contrato con `-q -p no:cacheprovider` (exit 0)
9. `git diff main...HEAD --` sobre GUARDIAS-CLAUDE, HOLDOUT-EXPOSICIONES, PROJECT_STATE, `test_guardia_g1.py` y `medir_g1.py`
10. `grep -E "SELLO|PICO DE MEMORIA| passed| failed" make-check.log`; `git rev-parse HEAD^{tree}`
11. `git rev-parse --verify -q refs/remotes/origin/fix/guardia-falsos-positivos`
12. Grep de `generar_capa.py` (:359 y :364)
13. `diff` de las dos respuestas del consultor, encargo contra informe → IGUALES las dos
14. `git diff --numstat 6a310dc8 HEAD -- docs/encargos/…`; `git diff --name-status main...HEAD`; `git log … -- knowledge/spec knowledge/cases` (vacío)
15. `uv run pytest tests/unit/test_guardia_falsos_positivos.py -q -p no:cacheprovider -rs`, y con `-v` → «51 passed», sin saltados
16. `uv run pytest … -o console_output_style=classic` → **NEGADO** (`pytest -o`). No lo reescribí con `-o`; usé `-v`.
17. `ls -d /c/Users/USER/gfp-* | wc -l` → 0
18. `uv run python -c` con los predicados F1 (`_comentario_que_no_es_ruta`, `_sufijos_tras_separador`) sobre cuatro literales. El primer intento falló por un error mío (el módulo sin `sys.modules`), no por la guardia.
19. `git diff --numstat main...HEAD --` de HISTORIA, GUARDIAS-CLAUDE y HOLDOUT-EXPOSICIONES; `wc -c PROJECT_STATE.md`
20. `grep` de las filas de HOLDOUT-EXPOSICIONES por fecha y rama, y de las de laminas
21. `git log --format='%h %ad'` de la rama y de capa-generada; `ls -l` de `make-check.log`
22. `git log`/`git diff f9888a03 HEAD -- docs/validation/GUARDIAS-CLAUDE.md`
23. `sed -n '215,221p' docs/validation/ACTIVAR-SESION-06-MOTOR.md`; `grep -n G.6 docs/plan/HOJA-DE-RUTA.md`
24. `grep -n "^## "` de CAPA-GENERADA.md y del informe

Ficheros:
- C:\Users\USER\Desktop\Bot v3\.claude\hooks\guardia.py
- C:\Users\USER\Desktop\Bot v3\tests\unit\test_guardia_falsos_positivos.py
- C:\Users\USER\Desktop\Bot v3\docs\validation\GUARDIA-FALSOS-POSITIVOS.md
- C:\Users\USER\Desktop\Bot v3\docs\validation\GUARDIAS-CLAUDE.md
- C:\Users\USER\Desktop\Bot v3\docs\validation\HOLDOUT-EXPOSICIONES.md
- C:\Users\USER\Desktop\Bot v3\docs\validation\anexos\GUARDIA-FALSOS-POSITIVOS\medida_parada2.py
- C:\Users\USER\Desktop\Bot v3\docs\encargos\trabajo-guardia-falsos-positivos.md

## Orden de cierre

Del consultor, 2026-11-13. Copiada tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Orden de cierre de trabajo/guardia-falsos-positivos (consultor, 2026-11-13). Revisada: se cierra con F2 y G.6, y F1 aplazado. Aplícala en este orden: el punto 1 ahora; del 2 en adelante, con la skill cerrar-rama cuando Aleks escriba /cerrar-rama trabajo/guardia-falsos-positivos.
>
> 1. Antes del cierre, el ensayo de D7 y un commit propio de la rama.
>  a. Si el ensayo o el cierre caen en un día que no es el 2026-11-13, lo primero de ese día, antes de cualquier make check, es la fila de HOLDOUT-EXPOSICIONES con su fecha (la lección A1 de esta rama). En main, tras el tag, ya no se puede añadir.
>  b. El ensayo, con la tabla de «El ensayo del cierre (D7), preparado para Aleks» sobre el último commit (82b19680), con el paso 5 en la rama (switch trabajo/guardia-falsos-positivos antes del git rm). Pásame una a una las órdenes que llevan «!» cuando toquen, y espera a que te diga que salieron. Lo que tiene que salir en verde en el clon: el make check del paso 9 con exit 0 y ningún failed; test_la_referencia_es_un_tag_y_no_es_esta_guardia y test_la_comparacion_caso_a_caso_con_la_guardia_de_main pasando sobre el árbol fusionado, con la línea del log que demuestra que no salieron saltados; y test_guardia_falsos_positivos.py con 6 xfailed y ningún failed. Si algo sale rojo en el clon, PARADA. Al terminar, el clon lo borro yo con «!».
>  c. Un commit propio de la rama («docs(guardia-falsos-positivos): el ensayo del cierre y la orden de cierre») con: esta orden copiada tal cual al final del informe, bajo «Orden de cierre»; las órdenes del ensayo como se lanzaron, el exit, el recuento y la línea PICO DE MEMORIA del log; «Lo que este ensayo no cubre» (pre-merge-commit, porque un clon nuevo no trae hooks, y el contenido del commit del contrato), como en GUARDIA-G1.md §13.7; y la corrección de la frase del paso 10 («sin contrato no hay SELLO»: make check sella igual, solo que nadie lo exige en el clon). make check sellado, push a fix/guardia-falsos-positivos y su CI (solo el fallo aceptado). Responde con el sha, el SELLO y el run, y espera a que Aleks escriba /cerrar-rama.
>
> 2. Tag: stable/F39a-guardia-falsos-positivos. Verifica en HISTORIA que el último es stable/F38z-capa-generada y que el tag no existe ni en local ni en origin (git ls-remote --tags origin stable/F39a-guardia-falsos-positivos, vacío). Mensaje del merge, sin comillas dobles dentro: «merge: trabajo/guardia-falsos-positivos, cmp de dos ficheros que no son guiones ya no se niega (G.6); el literal // de un guion nuevo, aplazado».
>
> 3. El commit del contrato (chore(cierre): sale el contrato y entra el registro en HISTORIA), en la rama. Con él, git log main..trabajo/guardia-falsos-positivos da 9 commits: 6a310dc8, dce4004e, f9888a03, 32316acf, 55d41a02, 5f757439, 82b19680, el del punto 1c y este. Toca PROJECT_STATE aunque la Next Action no cambie, por la línea de Technical Debt: que la puerta de git status del RITUAL lo espere.
>  - Sale contrato.yaml.
>  - Entra en HISTORIA el registro del cierre, con stable/F39a-guardia-falsos-positivos^{commit} en lugar del sha, los nueve commits, las filas de HOLDOUT-EXPOSICIONES de la rama (la del 2026-11-12, la del 2026-11-13, escrita tarde como ella misma dice, y la del punto 1a si hizo falta), los runs de la CI de fix/ (43366719378 sobre f9888a03, 43379762621 sobre 5f757439, 43386236034 sobre 82b19680 y el del punto 1c, todos con solo el fallo aceptado), y el ensayo del cierre con su sha, su SELLO y su run.
>  - Next Action: no sale ni entra ninguna letra.
>  - Technical Debt: la línea que entró con F38z (hacia :84) se sustituye por la de «Lineas para el cierre (simuladas)», tal cual. La de F38w (con $'\r', hacia :152) no cambia.
>  - Hoja de ruta, G.6: «Hecho cuando» se queda, y se añade debajo, con la forma de G.3 y G.5: «- **Estado:** HECHA (`trabajo/guardia-falsos-positivos`, `stable/F39a-guardia-falsos-positivos`; GUARDIA-FALSOS-POSITIVOS.md): cmp está en NO_EJECUTAN y sus argumentos se miran como una lectura, como los de diff (test_roto_sin_cmp_en_no_ejecutan).».
>  - wc -c PROJECT_STATE.md por debajo de 25.000 bytes (lo previsto: unos 24.787 en la rama y unos 24.555 en main). Si no, PARADA antes del commit.
>  - ERRORES-RECURRENTES, la fila de la rama, con el formato de la de trabajo/capa-generada:
>    · Revisor: opus, dos pasadas enteras. La primera, sobre 32316acf («Anexo · El informe del revisor (primera pasada)»): eje (a) 0 bloquea, 0 importa y 0 menores; eje (b) 2 bloquea (B1, B2), 3 importa y 2 menores; contestada en 55d41a02 y 5f757439 («Lo que se hizo con los hallazgos del revisor»); B1 y B2 se arreglaron en 5f757439 y se retiraron después con F1. La segunda, sobre 5f757439 («Anexo · El informe del revisor (segunda pasada, entera)»): eje (a) 0 bloquea, 1 importa (A1) y 2 menores; eje (b) 1 bloquea (B-1, F1 roto por R1-R4), 1 importa y 3 menores; contestada en 82b19680 («Lo que se hizo con los hallazgos de la segunda pasada del revisor»).
>    · Consultor (orden de cierre del 2026-11-13; consultor en Opus 5.5): 1 importa y 3 menores. Importa: D1 tal como estaba escrita dejaba pasar ocho casos que la guardia de stable/F38z niega (h1-h8), contra su propia D3; y después aceptó D1d y el arreglo de la PARADA 2 sin pedir antes un intento de romperlos, y el revisor los rompió dos veces (B1-B2 y R1-R4). Menores: D5 rompía test_roto_la_comparacion_con_main; la deuda de « / » y </li> se atribuyó a F38y y es de F38w; $'\r' se metió en el mismo mecanismo y es la comilla ANSI-C de tokenizar.
>    · Lecciones. Para el revisor: en una condición que exime parte de un literal, intentar romperla desde la primera pasada con lo que el código hace al ejecutarse (un recorte, un cd, un replace); aquí eso llegó en la segunda. Para el consultor: antes de aceptar una condición así, pedir una pasada que intente romperla, y si cae dos veces, aplazar (como aquí, punto 4 de la respuesta a la PARADA 2). De la sesión: la fila de HOLDOUT-EXPOSICIONES del día se escribe antes del primer make check del día, no después (A1).
>
> 4. El commit de estado en main solo sustituye Current Branch, Current Feature, Stable Main State y Last Stable Commit. La Next Action no cambia.
>
> 5. make check sellado, push atómico de main y el tag en un solo comando (Aleks confirma con «1. Yes»), CI de main en verde, y después borrar la rama local trabajo/guardia-falsos-positivos y la remota fix/guardia-falsos-positivos (git ls-remote --heads origin fix/guardia-falsos-positivos, vacío).
>
> 6. Informe final: sha de main, tag, run de la CI de main con su conclusion, ramas que quedan, el siguiente tag (F39b) y el tamaño de PROJECT_STATE.md; si pasa de 24.000 bytes, dilo: la rama de la activación de la 7a recorta antes de añadir.
