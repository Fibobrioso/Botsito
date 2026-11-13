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
tocarla: 15 fallos, cada uno por el motivo que dice
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

## Estado

EN CURSO (respuesta a la PARADA aplicada: el cambio de la guardia y sus tests; faltan fix/, el revisor y el ensayo del cierre).
