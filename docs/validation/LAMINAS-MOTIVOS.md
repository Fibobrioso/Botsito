# FUNCTIONALITY VALIDATION REPORT

**Funcionalidad:** F (1) · las frases de causa de las láminas (corrige R4.5)
**Rama:** trabajo/laminas-motivos
**Objetivo:** que ninguna lámina dé al trader una causa falsa o dudosa como cierta de por qué el bot no coloca, y regenerar las láminas de la 7a con el arreglo (encargo en `docs/encargos/trabajo-laminas-motivos.md`).

## Base (comprobada con git al abrir)

- `git rev-parse main origin/main`: `b52a7602cd9de0197a2a169b4027f542e7e29530` las dos veces.
- Último `- Tag:` de HISTORIA: `stable/F38x-preparacion-sesion-7`; `git rev-parse "stable/F38x-preparacion-sesion-7^{commit}"` = `git rev-parse main^1` = `526014743d0e8ac050b9f6d84a0a7a30667380aa`; en origin (`git ls-remote --tags`: `3643625…` refs/tags/stable/F38x-preparacion-sesion-7).
- CI de main sobre `b52a7602cd9de0197a2a169b4027f542e7e29530` (`gh run view 43145636325`): workflow `ci`, `completed`, `success`.
- `git branch --list`: solo `main`; `git ls-remote --heads origin`: solo `refs/heads/main`; ninguna `fix/*`.
- `PROJECT_STATE.md` en main: 23.914 bytes (`wc -c`).

## Fase 0

Sin código: solo este informe y las dos filas de `HOLDOUT-EXPOSICIONES.md` (2026-11-11 y
2026-11-12). Los guiones de medida están en la carpeta de trabajo de la sesión, fuera del repo,
porque uno de ellos lee `clave.txt`.

### 0.1 · Cada gate de MOTIVO_GATE frente a su forma

Las formas salen de `knowledge/spec/strategy_spec.yaml`, volcadas con un guion que imprime el
`cuando` de cada regla VIGENTE con `prohibe`. Son 15, las mismas claves que `MOTIVO_GATE`
(`laminas.py:568-585`); eso ya lo comprueba `test_la_tabla_de_gates_es_la_de_las_vigente_que_prohiben`.

Quién enciende cada hecho de detención: en la spec solo hay cinco acciones `fijar` sobre
`detenido_por_*`:
- RN-016, `detenido_por_cartuchos` (:1912);
- RN-020, `detenido_por_tope` (:2116);
- RN-036, `detenido_por_racha` (:2179);
- RN-029, `detenido_por_tope` (:2427);
- RN-031, `detenido_por_tope_total` (:2532).

Además, `abrir_escenario` (RN-004) apaga `detenido_por_cartuchos`. Un hecho nunca es «desconocido»:
`Interprete._hecho` da SI o NO (`interprete.py:183-202`). Solo un predicado puede dejar un gate en
desconocido.

| Gate | Forma y ramas | Quién enciende cada hecho de la forma | Frase de hoy | Cubre |
|---|---|---|---|---|
| RN-001 | `cualquiera_de`: (1) `ninguno_de en_ventana` (fuera de la ventana), (2) `hecho detenido_por_tope`, (3) `hecho detenido_por_tope_total`, (4) `hecho detenido_por_cartuchos` | (2) RN-020 o RN-029; (3) RN-031; (4) RN-016 | «está fuera de la ventana de la sesión» | **no**: solo cubre la rama 1; con la 2, la 3 o la 4 es falsa |
| RN-037 | `todos_de`: `en_el_ultimo_tramo_h4` | — | «es el último minuto antes de que cierre la vela H4 de la sesión» | sí |
| RN-033 | `cualquiera_de`: `sesgo = ambiguo`, `sesgo = insuficiente` | `sesgo` lo fija RN-003 (no es de detención) | «no hay sesgo de H4 claro» | sí: las dos |
| RN-005 | `todos_de`: `hecho sesgo` (liga S), `se_desarrolla_en_el_lado_de_ruido` | — | «lo que se forma queda en la zona de ruido de la liquidez de M15, donde no se busca entrada» | sí |
| RN-008 | `todos_de`: (1) `ninguno_de` de los dos `se_da_esquema`, (2) `ninguno_de la_orden_nace_antes_del_esquema` | — | «no se da ninguno de los dos esquemas de entrada» | **parcial**: nombra (1). Cuando dispara, (2) también se cumple, así que lo que dice es cierto pero incompleto. Con el valor de hoy, `orden_limite_nace = al_aparecer_punto_de_breaker` (`parametros.yaml`), (2) da NO y RN-008 no dispara nunca (`zonas.py:571-576`; ADR-0056 §7, ADR-0064) |
| RN-009 | `todos_de`: `zonas_desarrolladas_superan` | — | «el esquema tiene más zonas de control de las que admite ({n}, y admite {m})» | sí |
| RN-016 | `cualquiera_de`: (1) stop + `alcanza_tope cartuchos`, (2) pérdida + `alcanza_tope cartuchos`, (3) `hecho detenido_por_cartuchos` | (3) solo RN-016 | «ya ha gastado sus intentos en esta liquidez» | sí: las tres ramas son «gastó sus intentos» |
| RN-018 | `todos_de`: `operaciones_abiertas_alcanzan` | — | «ya tiene una operación abierta, y no opera en paralelo» | sí |
| RN-020 | `cualquiera_de`: (1) `alcanza_tope perdida_dia`, (2) `alcanza_tope perdida_semana`, (3) `hecho detenido_por_tope` | (3) RN-020 **o RN-029** | «ha llegado a la pérdida máxima del día del trader» | **no**: con (3) encendido por RN-029 es falsa. La rama (2) ya la descarta `ALCANCES_SOLO_DIA` (`_motivo`, :1013-1014) |
| RN-036 | `cualquiera_de`: `alcanza_tope racha_perdidas`, `hecho detenido_por_racha` | solo RN-036 | «viene de la racha de pérdidas seguidas del trader» | sí |
| RN-022 | `todos_de`: `ninguna_regla_de_entrada_aplica` | — | «la situación no encaja en lo que sabe hacer» | sí |
| RN-026 | `todos_de`: `distancia_menor_que` | — | «el bróker no admite el stop donde toca» | sí |
| RN-029 | `cualquiera_de`: (1) `se_acerca_al_limite perdida_dia_firma`, (2) `hecho detenido_por_tope` | (2) RN-029 **o RN-020** | «ha saltado el freno diario de la cuenta» | **no**: con (2) encendido por RN-020 es falsa |
| RN-031 | `cualquiera_de`: `se_acerca_al_limite perdida_total_firma`, `hecho detenido_por_tope_total` | solo RN-031 | «ha saltado el freno total de la cuenta» | sí |
| RN-032 | `cualquiera_de`: `no_cabe_la_operacion` sobre `perdida_dia_firma` y sobre `perdida_total_firma` | — | «el riesgo de la operación no cabe antes del límite de la cuenta» | sí: dice «el límite» sin decir cuál |

El auditor del consultor acertó en RN-001, RN-020, RN-029 y RN-008, y ninguna otra frase nombra
un caso. Con un matiz que mide el auditor de la rama (fila 13): con `detenido_por_tope` encendido,
RN-020 y RN-029 disparan las dos por la rama del hecho, porque las dos lo leen y lo reescriben en
cada evento (spec:732-741). No es que cada una «pueda» salir con la frase de la otra: una de las
dos frases sale falsa siempre, salvo que se den los dos topes a la vez.

### 0.2 · La rama activa de RN-001 en las láminas 09 y 10 de la sesión 6 de la 7a

Se midió con una invocación de `motor decisiones`, con la bitácora de los seis días de la 7a y sin
`--meses`, que es la misma corrida de construcción que `motor laminas`. La salida fue a
`data/laminas-motivos/bitacora`, que git ignora, y tardó 596 s con un pico de 638 MiB. La lee un
guion que cruza cada lámina de `clave.txt` con la bitácora de su día en el cierre de su corte, y
que solo imprime el código de la lámina. Sobre las horas: la lámina dice «Corte: a las 14:09, al
cierre de la vela de M1 de las 14:08», y la bitácora rotula cada línea con el cierre, así que las
líneas que corresponden son las de 14:09 y 14:23 (auditor, fila 26).

En la sesión 6 de la 7a (11:00-15:00), la bitácora da esto:
- **14:08** (cierre de la M1 de las 14:07): `hecho detenido_por_cartuchos: - -> hasta_cartuchos_reinicio (RN-016)`
  y, en el mismo cierre, `prohibido buscar_entradas por: RN-001 [dispara]`.
- **14:09** (lámina 09) y **14:23** (lámina 10): `RN-015 no ejecuta accion:colocar_orden_limite
  (prohibida:abrir_operacion): la prohiben RN-001 [dispara], RN-009 [dispara], RN-016 [dispara]`.
  `detenido_por_cartuchos` sigue encendido, y ningún cambio de hecho lo apaga entre 14:08 y 14:23.

**La rama activa de RN-001 en los dos cortes es la (4), `detenido_por_cartuchos`, encendido por
RN-016 a las 14:08.** La rama (1), fuera de la ventana, no se da: 14:09 y 14:23 caen dentro de la
sesión 11-15 y de la ventana 07:00-15:00. Las ramas (2) y (3) tampoco: en todo el día no se
enciende ningún otro `detenido_*`. Así que «está fuera de la ventana de la sesión» es falsa en las
dos láminas, y la causa cierta es la que ya dice la línea de RN-016.

### 0.3 · Cuántas láminas de la 7a llevan una causa de gate falsa o dudosa como cierta

**Contado contra los HTML** (`grep` de «Iba a colocar la orden y no la coloca» y de «No abre» en
las 38 láminas): hay 18 causas de gate en 11 láminas. Son 11 de RN-009, 3 de RN-005, 2 de RN-016
y 2 de RN-001, y ninguna sale por la vía de «No abre».

**Contado contra la bitácora**, porque el HTML no lleva el `t` del par (auditor, fila 28: un gate
desconocido sale con el mismo texto que uno que dispara): en el corte de cada una de esas 11
láminas, los gates que bloquean la colocación son exactamente los de su HTML, y **todos con
`[dispara]`**. En los seis días no hay ningún `[desconocido]` en ningún corte de lámina.

| Qué | Láminas |
|---|---|
| Frase de gate que no cubre su rama activa | **2**: sesion-06, láminas 09 y 10 (RN-001) |
| Gate «desconocido» dicho como cierto | **0** (medido con la bitácora, no con los HTML) |
| RN-020, RN-029 o RN-008 en alguna lámina | 0 |

Las 16 causas restantes son de gates de una sola condición (RN-009, RN-005) o de RN-016, cuya
frase cubre sus tres ramas.

### 0.4 · El arreglo que propongo

**De dónde sale la rama activa.** El intérprete no la registra: `Evento` no tiene ese campo
(`interprete.py:116-141`), y el contrato protege `interprete.py`, `decisiones.py` y `cableado.py`
(«qué no cambia»). Así que la lámina la deduce de su foto, sin tocar el motor:
- **Ramas que son un hecho de detención**: el hecho está en `f.hechos` y quién lo encendió, en
  `f.origen`. Es lo que ya hace `FRASE_TOPE_POR_REGLA` (`laminas.py:795-803`). Los hechos solo se
  apagan al abrir sesión, al principio del evento (`interprete.py:333-336`), y con
  `abrir_escenario`, que RN-001 bloquea porque prohíbe `buscar_entradas`. Por eso un hecho que
  disparó un gate en el evento sigue en la foto, que se toma al final del cierre.

  > **CORRECCIÓN (revisor, a1; el texto de arriba no se toca).** El argumento falla en dos cosas.
  > Primera: `abrir_escenario` no declara `efecto` (`strategy_spec.yaml:471-481`; la única acción
  > con `efecto` es `colocar_orden_limite`, :448), y el intérprete solo bloquea las acciones que lo
  > declaran (`interprete.py:281-291`). Así que RN-004 PUEDE apagar `detenido_por_cartuchos` en
  > el mismo evento en que RN-016 o RN-001 ya dispararon por ese hecho, y la foto sale sin él.
  > En ese caso la lámina no dice una frase falsa: da `LaminaError` (la regla que dispara sin su
  > hecho, o RN-001 sin ninguna rama identificable), y `motor laminas` no escribe nada. En las
  > seis sesiones de la 7a no pasó (F2). Es un riesgo para las láminas de la 7b y va en «Lo que
  > no me convence» de la PARADA final. Segunda: el contrato protege `interprete.py` y
  > `decisiones.py`, pero no `cableado.py`; a este lo cubre «qué no cambia» del encargo (el motor).
- **Ramas de acumulador de RN-020 y RN-029**: cuando cualquiera de las dos dispara, en ese mismo
  evento fija `detenido_por_tope`. Su frase sale siempre del origen de ese hecho; si el hecho no
  está en la foto, `LaminaError`.
- **La rama de la ventana de RN-001**: se da si el corte cae fuera de los límites de sesión de la
  foto (`f.limites`, del mismo reloj de las sesiones). Un test comprueba que la unión de las
  sesiones del kit es la ventana del registro (`ventana_inicio` y `ventana_fin`). Si RN-001 dispara
  y no se identifica ninguna de sus cuatro ramas, `LaminaError`.

**La tabla.** `MOTIVO_GATE` pasa a ser un dict de cada gate a sus ramas. Cada rama tiene su frase,
o la marca «la frase sale del origen del hecho». Los gates cuya frase cubre todas sus ramas (RN-016,
RN-031, RN-036, RN-033, RN-032 y los de una condición) declaran sus ramas con la misma frase. Así
la tabla es completa por construcción, y la guardia (b) es un test que compara las ramas de la
tabla con las de la forma de la spec. Los hijos de `cualquiera_de` se cuentan uno a uno, y un
`todos_de` cuenta como una rama.

**Decisiones del consultor, punto por punto:**
- **a)** La frase sale de la rama activa, y la de un hecho, de `f.origen`: con
  `detenido_por_tope` es la de su regla de origen (RN-020: «ha llegado a la pérdida máxima del día
  del trader»; RN-029: «ha saltado el freno diario de la cuenta»). Con
  `detenido_por_tope_total`, «ha saltado el freno total de la cuenta». Con
  `detenido_por_cartuchos`, «ya ha gastado sus intentos en esta liquidez».
- **b)** Un gate de varias ramas sin frase para la que está activa, un hecho con origen vacío,
  desconocido o múltiple, o un gate que dispara sin ninguna rama identificable: `LaminaError`.
- **c)** Varias ramas activas: una frase por rama. **Una rama que es un hecho cuya regla de origen
  ya está en la lista de causas no se repite**, porque esa regla ya lo dice. Además, nunca salen
  dos causas con el mismo texto. En las láminas 09 y 10 desaparece la línea de RN-001 y quedan las
  de RN-009 y RN-016 en su orden. Con un tope de RN-029, RN-020 no dice nada (su rama es el hecho
  de RN-029, que ya está en la lista) y RN-029 dice la suya.
- **d)** Un gate con `t = desconocido` en `f.bloqueos` sale como «Iba a colocar la orden y no la
  coloca porque no puede descartar que {motivo}.», con la forma de `FRASE_PROHIBE["desconocido"]`.
  El motivo es el de sus ramas de predicado, porque las ramas de hecho nunca son desconocidas. Si
  esas ramas tienen frases distintas en la tabla, `LaminaError` (hoy no pasa en ningún gate).
- **e)** La vía de `f.prohibido` usa la misma rama activa, y la de `f.quizas`, el mismo motivo
  dudoso de d).
- **f)** RN-008: punto 0 de las decisiones.

**Tests de F1, con los matices del auditor:**
- El test (2) pone RN-020 **y** RN-029 en `f.bloqueos`, como en el motor real (fila 29). Si no,
  pasa en main y no prueba nada.
- `test_ninguna_frase_lleva_ids_dinero_ni_fechas` hoy deja fuera en silencio `MOTIVO_GATE`,
  `LIMITE_NO_ENVIO` y `LADO_TOMA`. Los descarta su filtro «empieza en mayúscula y acaba en punto»
  (`test_laminas.py:530`), y además no baja a un dict dentro de otro. El arreglo recorre cada
  cadena de cada tabla a cualquier profundidad, sin filtro, y comprueba que el recuento de cadenas
  revisadas cuadra con uno contado aparte.

**Lo que espero en v2** (se comprueba en F2): solo cambian las láminas 09 y 10 de sesion-06, a las
que les sobra la línea de RN-001; las otras 36 quedan idénticas byte a byte.

## El encargo frente al repo (auditor-encargo)

El auditor contó 39 afirmaciones: 25 correctas, 1 incorrecta y 13 con matiz, más 3 herencias no
recogidas. Lo que cambia algo:
- **INCORRECTA (fila 28)**: los «desconocidos» no se pueden contar en los HTML, porque el par
  `(g, t)` se pierde en `laminas.py:1057`. Se midieron con la bitácora (0.3), y por eso hizo falta
  la clave.
- **Matiz (fila 13)**: RN-020 y RN-029 salen siempre juntas con el hecho encendido (0.1).
- **Matiz (fila 20)**: el contrato deja fuera `tests/unit/test_laminas_svg.py`, donde viven
  `foto_base` y los tests de frases de gates que el arreglo puede tocar. Va en las decisiones
  (punto 1).
- **Matiz (fila 29)**: el test F1 (2) tiene que poner las dos reglas en la foto (0.4).
- **Matiz (fila 30)**: el test de frases ya no revisaba `MOTIVO_GATE` (0.4).
- **Matiz (fila 32)**: la frase nueva de F3 choca en la letra con «Ningún resultado se enseña» de
  ADR-0093 §3 y de PREGUNTAS-7A.md:69 (punto 3 de las decisiones).
- **Matiz (fila 33)**: el SVG mide 1.600 y el `body` lleva 24 px de margen a cada lado
  (`laminas_svg.py:58`, :521), así que la lámina entera pide 1.648 px y no 1.624 (punto 4).
- **Matiz (filas 7 y 36)**: R4.5 está HECHA y ninguna entrada de la hoja de ruta recoge este
  arreglo. PROJECT_STATE ya está en 23.916 bytes (+2) por la apertura.
- **Herencias**:
  1. los recuentos por carpeta de F2 frente a la clave (punto 2 de las decisiones);
  2. LAMINAS.md, informe cerrado, da en su tabla la frase de RN-001 que se cambia (punto 5);
  3. la hoja de ruta en el cierre (punto 6).

## Lo que no pude medir

- Que la bitácora y la lámina pinten las horas en el mismo huso no está medido aparte. Los cortes
  de `clave.txt` (Europe/Madrid) casan línea a línea con los bloqueos de la bitácora en las 11
  láminas con causas, y eso lo sostiene.
- No hay ninguna foto real con `detenido_por_tope`, `detenido_por_tope_total` ni un gate
  desconocido en las láminas de la 7a. Esas ramas se prueban con fotos de test.

## Exposiciones

Las dos filas de `HOLDOUT-EXPOSICIONES.md`:
- **2026-11-11**: el `make check` de la apertura, la lectura entera de `clave.txt` y el `grep` de
  los HTML. Se escribió pasada la medianoche, porque durante el `make check` no se escribe en el
  árbol; se dice.
- **2026-11-12**: la bitácora, declarada antes de lanzarla.

De los días reservados, solo el M1 de marzo y de junio con que calientan la bitácora y cada
`make check`, como siempre (Technical Debt). Ninguna transcripción y ningún fotograma.

## Lo que necesito que decidas

0. **RN-008 (decisión f).** Opciones: (a) dejar su frase, que es cierta aunque incompleta, y
   declarar sus dos condiciones en la tabla con la misma frase; (b) completarla: «no se da ninguno
   de los dos esquemas de entrada, y la orden no nace antes del esquema». Recomiendo (a): cuando
   dispara, lo que dice es verdad, y con el valor de hoy de `orden_limite_nace` RN-008 no dispara
   nunca. Coste de (b): una frase con jerga del motor («la orden nace antes») que el trader no usa,
   para un gate que hoy no sale.
1. **Ampliar el contrato a `tests/unit/test_laminas_svg.py`.** Opciones: (a) ampliarlo en el
   primer commit de F1, dicho en el informe; (b) no tocarlo y escribir los tests nuevos sin
   `foto_base`. Recomiendo (a): ahí están `foto_base` y los tests de frases de gates
   (`test_laminas_svg.py:274-290`, :354-364, :373-384). Si alguno cambia por el arreglo, tiene que
   poder cambiar en la misma rama. Coste de (b): duplicar la fábrica de fotos y arriesgar un test
   viejo en rojo que no se puede arreglar.
2. **Los recuentos por carpeta de F2** («cuántas láminas cambian y en qué carpeta y número»).
   Opciones: (a) publicarlos en el informe como pide el encargo; (b) dar en el informe solo el
   total y que lo demás vaya a Aleks fuera del repo. Recomiendo (a): un número de lámina no da
   ninguna fecha, el encargo ya nombra sesion-06, láminas 09 y 10, y con ADR-0093 §2 el trader
   carga él mismo el día (fila del 2026-11-11 de HOLDOUT-EXPOSICIONES, punto 2). Coste de (a): lo
   que ERRORES-RECURRENTES.md:117-118 ya señaló, que cruzado con PREGUNTAS-7A.md estrecha la clave.
3. **La frase nueva de F3 frente a «Ningún resultado se enseña»** (ADR-0093 §3 y
   PREGUNTAS-7A.md:69). La frase dice que la lámina siguiente enseña cómo acabaron las anteriores.
   Opciones: (a) entra tal cual y «Ningún resultado se enseña» pasa a leerse como «ningún resultado
   posterior al corte» (es lo que LAMINAS.md, «Quedan fuera de la lámina», ya aprobó), dicho en el
   informe; (b) que el consultor reescriba una de las dos frases. Recomiendo (a), con una aclaración
   en el mismo paso 4: «ningún resultado posterior al corte de la lámina que se enseña». Coste de
   (b): otra vuelta antes de grabar la 7a.
4. **El ancho de F3**: 1.624 o 1.648 píxeles. Opciones: (a) 1.648, el SVG más los dos márgenes;
   (b) 1.624 como dice el encargo. Recomiendo (a): con 1.624 el SVG entra entero, pero el margen
   derecho no, y sale barra horizontal. Coste de (a): ninguno.
5. **LAMINAS.md (informe cerrado en main) da a RN-001 la frase que se corrige.** Opciones: (a)
   ponerle un recuadro de corrección junto a su tabla de causas, con fecha y rama
   (CLAUDE.md, «Regímenes de cambio»), ampliando el contrato a ese fichero; (b) no tocarlo y que lo
   diga solo este informe. Recomiendo (a): es la práctica escrita para un informe cerrado que queda
   mal. Coste de (b): LAMINAS.md sigue diciendo una frase que el código ya no da, sin aviso.
6. **La hoja de ruta.** Opciones: (a) en las líneas de cierre, una frase en R4.5 HECHA que remita a
   este informe; (b) nada. Recomiendo (a), y que la escriba el cierre, porque el contrato protege
   la hoja en la rama. Coste de (b): la hoja no dice que R4.5 se corrigió antes de la 7a.

## Respuesta del consultor a la PARADA de la fase 0 (2026-11-12)

Copiada tal cual:

> Modelo: Opus 5.5 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 de trabajo/laminas-motivos (2026-11-12). Cópiala tal cual al final del encargo y del informe, con su fecha, y aplícala punto por punto (skill fase-cero). Buena fase 0: las cuatro desviaciones de «Lo que cambia» quedan aceptadas (la rama se deduce de la foto, con LaminaError si no se identifica; el test F1 (2) con RN-020 y RN-029 juntas en la foto, que es el caso real; el arreglo del filtro del test de frases dentro de F1; y lo que esperas en v2). La fila de exposiciones del 2026-11-11 escrita pasada la medianoche queda aceptada como desviación declarada: lo que se leyó (clave.txt) son días de construcción.
>
> 0. RN-008: de acuerdo. La frase se queda, y el informe y la tabla de 0.1 declaran sus dos condiciones y que con el valor actual de orden_limite_nace no dispara.
> 1. De acuerdo: el contrato se amplía a tests/unit/test_laminas_svg.py.
> 2. Publícalos. Con ADR-0093 §2 el trader carga él mismo el día, así que la clave ya no protege ninguna fecha que él no vea. Es lo mismo que se decidió en el cierre de F38x (respuesta a su PARADA final, punto 3), y la fase 0 ya los nombra.
> 3. Que entre la frase, pero la regla se aclara en el ADR, que es la fuente, y no solo en la hoja: un recuadro fechado en ADR-0093 §2, con la forma de los recuadros de ADR-0084. Su texto: «"Ningún resultado se enseña" quiere decir ningún resultado posterior al corte. Lo que la lámina dice de cómo acabaron las órdenes anteriores de la misma sesión ("Antes, en esta sesión: …") es el estado del bot en el instante del corte (sus intentos, RN-016) y se enseña, porque explica la decisión. Por eso las láminas de una sesión se enseñan en su orden, y el trader corrige cada una antes de ver la siguiente.» El paso 4 de PREGUNTAS-7A.md dice «ningún resultado posterior al corte» y remite al recuadro. El contrato se amplía a docs/adr/0093-*.md, solo con ese recuadro.
> 4. De acuerdo: 1.648 píxeles, medido.
> 5. De acuerdo: recuadro de corrección en docs/runbooks/LAMINAS.md, en su tabla, y el contrato se amplía a ese fichero.
> 6. De acuerdo: en el cierre, una frase en R4.5 que remita a LAMINAS-MOTIVOS.md, comprobada con problemas_a a problemas_d.
>
> Sigue sin parar con F1, F2 y F3 y la PARADA condicional: solo paras si v2 cambia algo más que la línea de RN-001 de sesion-06/09 y sesion-06/10, si una foto de las seis sesiones da LaminaError con el arreglo, o si una guardia niega algo legítimo. Después, el revisor con sus cuatro alcances más uno: que el recuadro de ADR-0093 diga lo del punto 3 sin añadir ni quitar. Luego, la PARADA final con la ruta de C:\Users\USER\Desktop\laminas-sesion-7a-v2 y las líneas de cierre.
>
> Rama lista para revisión, NO cerrada.

## La respuesta, aplicada punto por punto

- **Las cuatro desviaciones y la fila del 2026-11-11**: aceptadas, sin más que hacer.
- **0. RN-008**: hecho. La frase se queda. La fila de 0.1 ya declaraba sus dos condiciones y que,
  con el valor actual de `orden_limite_nace`, RN-008 no dispara. En la tabla del código va como
  una sola rama (`sin_esquema`), con ese comentario.
- **1. Contrato**: hecho. `tests/unit/test_laminas_svg.py` entra en `rutas_permitidas`
  (`contrato.yaml`).
- **2. Recuentos por carpeta**: se publican en F2.
- **3. ADR-0093**: hecho. El recuadro va en §2, con la forma de los de ADR-0084 (cita en bloque y
  una cabecera en negrita con la fecha, la rama y de dónde sale, «el cuerpo no se toca»), con el
  texto del consultor sin cambiar una palabra. El paso 4 de PREGUNTAS-7A.md dice «Ningún resultado
  posterior al corte se enseña» y remite al recuadro. `docs/adr/0093-*.md` entra en el contrato.
  Una nota: en la PARADA cité la frase como «ADR-0093 §3». Está en §2, punto 3 de su lista, que es
  donde la pone el consultor.
- **4. Ancho**: hecho, 1.648 píxeles en el paso 4.
- **5. Recuadro de corrección en `docs/runbooks/LAMINAS.md`, «en su tabla»**: **no aplicado.
  PARADA 2, punto 0**. Lo medido lo contradice: `docs/runbooks/LAMINAS.md` no tiene ninguna tabla
  de causas ni nombra RN-001 (`grep -n "RN-001\|fuera de la ventana"` no da nada en él). La tabla
  que da a RN-001 «está fuera de la ventana de la sesión» es la del informe cerrado
  `docs/validation/LAMINAS.md` (:108, y :139 en la de la lista de causas). El error es mío: en la
  PARADA escribí «LAMINAS.md (informe cerrado en main)» sin la ruta. No se ajusta en silencio, así
  que va a la PARADA final; el contrato sigue protegiendo `docs/validation/LAMINAS.md`.
- **6. Hoja de ruta**: en las líneas de cierre de la PARADA final.

## F1 · El arreglo en `laminas.py`, con sus tests

**El código** (`src/botsito/engine/laminas.py`):
- `MOTIVO_GATE` pasa a ser **un dict de cada gate a sus ramas**, en el orden de su forma: los hijos
  de su `cualquiera_de`, o una sola rama para un `todos_de`. Cada rama lleva su frase. La rama que
  es un hecho de detención lleva `None`: su frase sale de la regla que lo encendió (`f.origen`), a
  través de `MOTIVO_POR_ORIGEN` (las cinco reglas que fijan un `detenido_*`). `HECHO_QUE_FIJA` dice
  qué hecho fija cada una al disparar.
- `_motivos(gate, tipo, f, ciertos, …)` sustituye a `_motivo`:
  - Con `dispara`, devuelve la frase de cada rama activa. Una rama de hecho cuya regla de origen ya
    dispara en el cierre (`ciertos`) no se repite. La ventana de RN-001 se lee con
    `fuera_de_ventana(f)` (el corte fuera de todos los `f.limites`). Si ningún hecho está
    encendido, sale la frase común de las ramas de predicado.
  - Con `desconocido`, devuelve la frase común de las ramas de predicado.
  - Da `LaminaError` en estos casos: una rama sin frase, un hecho con frase propia, un hecho sin
    una regla de origen conocida, una regla de `HECHO_QUE_FIJA` que dispara sin su hecho en la
    foto, RN-001 que dispara dentro de la sesión y sin ningún hecho, o un gate desconocido cuyas
    ramas de predicado no comparten frase.
- `FRASE_BLOQUEO` pasa a ser un dict por tipo. Con `desconocido` dice «Iba a colocar la orden y no
  la coloca porque no puede descartar que {motivo}.», con la forma de
  `FRASE_PROHIBE["desconocido"]`. Un tipo sin frase da `LaminaError`.
- `_sin_orden` pasa cada gate de `f.bloqueos` con su `t` (antes tiraba el segundo campo) y cada
  gate de `f.prohibido` y `f.quizas` por `_motivos`. Nunca salen dos causas con el mismo motivo.

**Los tests** (`test_laminas_svg.py`, al final, y `test_laminas.py`):

| Test | Qué comprueba | En main |
|---|---|---|
| `test_con_los_intentos_gastados_rn001_no_dice_fuera_de_la_ventana` | F1 (1): `detenido_por_cartuchos` de RN-016, RN-001 y RN-016 en `f.bloqueos`, con el corte dentro de la sesión. No sale «fuera de la ventana» y los intentos salen una vez. Con RN-001 solo, los intentos los dice RN-001 | **rompe**: `assert not ['Iba a colocar la orden y no la coloca: está fuera de la ventana de la sesión.']` |
| `test_el_tope_de_una_regla_no_sale_con_la_frase_de_la_otra` (×2) | F1 (2): `detenido_por_tope` de RN-029 (y de RN-020), con RN-020 **y** RN-029 en `f.bloqueos` y en `f.prohibido`, como en el motor | **rompen** los dos: sale la frase de RN-020 con el tope de RN-029, y la de RN-029 con el de RN-020 |
| `test_un_gate_desconocido_no_sale_como_causa_cierta` | F1 (3): RN-005 `desconocido` en `f.bloqueos` sale como duda; RN-001 en `f.quizas`, también como duda | **rompe**: sale «Iba a colocar la orden y no la coloca: lo que se forma queda en la zona de ruido…» |
| `test_fuera_de_la_ventana_sigue_diciendo_fuera_de_la_ventana` | Lo que no cambia: con el corte fuera de toda sesión, RN-001 dice «está fuera de la ventana de la sesión» | **pasa** |
| `test_la_guardia_falla_si_se_quita_la_frase_de_una_rama` (×4: RN-001, RN-020, RN-016, RN-032) | La guardia nueva, que falla a propósito con la tabla mutada (`monkeypatch`, la frase de una rama a `None`): `LaminaError` | no se compara: en main la tabla por ramas no existe (lo dice el encargo) |
| `test_lo_que_no_se_identifica_falla_con_su_nombre` | Negar por defecto: RN-001 sin rama identificable, un hecho de un origen desconocido, RN-020 sin su hecho, un tipo sin frase | — |
| `test_las_ramas_de_cada_gate_son_las_de_su_forma` | Las ramas de la tabla, contra las de la forma de la spec: tantas, en el mismo orden, y las de hecho de detención, las mismas y sin frase. Una rama nueva en la spec lo rompe | — |
| `test_quien_fija_cada_hecho_de_detencion_es_lo_de_la_spec` | `HECHO_QUE_FIJA` y `MOTIVO_POR_ORIGEN`, contra las acciones `fijar` de la spec | — |
| `test_las_sesiones_del_kit_son_la_ventana_del_registro` | La unión de las sesiones del kit es [`ventana_inicio`, `ventana_fin`), y eso sostiene `fuera_de_ventana` | — |
| `test_ninguna_frase_lleva_ids_dinero_ni_fechas` (reescrito) | Cada cadena de cada tabla, a cualquier profundidad y sin filtro. Las de `MOTIVO_GATE`, contadas aparte, están todas. Una tabla que no aporte cadenas falla | en main revisaba 48 de las 70 que recogía; aquí revisa 80 |

**Cómo se comprobó «rompe en main»** (skill `comparar-con-main`): un clon desechable
`git worktree add --detach C:/cmlm/main main`, con `tests/unit/test_laminas_svg.py` de la rama
copiado dentro, y `uv run pytest tests/unit/test_laminas_svg.py -k …` ejecutado allí. Resultado:
los cuatro casos de F1 (1)-(3) en FAILED, con las aserciones de la tabla, y el de «fuera de la
ventana» en PASSED. El recuento de 48 de 70 sale de un guion de la carpeta de trabajo que repite
el filtro de main en ese clon. Los tests de F1 no leen nada de la tabla nueva: las frases van
literales, para que en main rompan por la frase y no por un nombre que falta. El clon se quitó con
`git worktree remove --force` (llevaba el test copiado sin commitear) y `git worktree prune`. En el
repo real no queda ninguna rama, tag ni ref remota nueva (158 tags antes y después; en origin, solo
`main`). La carpeta vacía `C:\cmlm` se queda: la comprobación de seguridad de Claude Code negó el
`rmdir`, y la quita Aleks.

**Un test viejo cambia** (`test_rn020_dice_del_dia_solo_si_la_rama_semanal_no_puede_disparar`): su
foto ponía RN-020 en `f.prohibido` sin el `detenido_por_tope` que RN-020 fija al disparar. Con la
guardia nueva eso es una foto que no cuadra, así que la foto lleva ahora el hecho con origen
RN-020, como en el motor. Lo que comprueba no cambia.

Los tests de láminas (`test_laminas.py`, `test_laminas_svg.py`, `test_laminas_registro.py`) y
`test_adr.py` pasan en la rama. `Tests Currently Passing` pasa de 2008 a 2017 funciones (+9).

## F2 · Las láminas de la 7a, regeneradas

La fila de exposiciones se escribió antes de lanzar nada. La orden, con las seis sesiones en el
orden de `clave.txt` de `laminas-sesion-7a` (no se escribe aquí):
`uv run botsito motor laminas --sesiones <las seis, en su orden> --salida <carpeta>`.
`motor laminas` solo escribe en `--salida` (`laminas.escribir`, `laminas.py:1425-1432`).

1. **Ensayo** en un clon desechable del commit `b735dc2b`
   (`git worktree add --detach C:/cmlm/rama HEAD`, con su `config/settings.local.toml` apuntando al
   `data/` real). La salida fue a la carpeta de trabajo de la sesión, y la corrida salió con 0 en
   465 s, con un pico de 644 MiB. La base, con el recolector y sin él, dio la misma tupla
   `(31, 192, 24, 1150, 0, 32, 0)`: el recolector sigue sin cambiar lo que decide el motor. Salieron
   las mismas 38 láminas por carpeta que la v1 (6, 5, 4, 9, 4 y 10). El clon se quitó con
   `git worktree remove --force` (llevaba su `settings.local.toml` sin seguir) y
   `git worktree prune`.
2. **La v2** desde el repo, a `C:\Users\USER\Desktop\laminas-sesion-7a-v2`, que no existía antes.
   Salió con 0 en 463 s, con un pico de 643 MiB y los mismos recuentos.

**v1 frente a v2**, fichero a fichero con sha256, con un guion de la carpeta de trabajo que no
imprime `clave.txt`:

| Qué | Resultado |
|---|---|
| `clave.txt` | idéntica (comparada por hash, sin imprimirla) |
| Ficheros, sin `clave.txt` | 44 en v1 y 44 en v2; ninguno solo en un lado |
| Idénticos byte a byte | **42**: los seis `indice.html` y 36 de las 38 láminas |
| Distintos | **2**: `sesion-06/lamina-09.html` y `sesion-06/lamina-10.html` |
| Qué cambia en cada una | una sola línea **quitada**, `<li>Iba a colocar la orden y no la coloca: está fuera de la ventana de la sesión.</li>` (diff `-1010 +1009,0` y `-1072 +1071,0`); nada más |

Es exactamente lo que se esperaba en 0.4, así que no se para. Recuentos en la v2, con `grep` de
los HTML:
- «fuera de la ventana de la sesión»: en **0** láminas (en la v1 eran 2);
- causas de gate: **16** líneas (en la v1 eran 18);
- causas dichas como duda: **0**.

El ensayo y la v2 dan la misma comparación. Ninguna foto de las seis sesiones dio `LaminaError`
con el arreglo.

## El encargo, punto por punto

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Abrir con `abrir-rama`, riesgo medio, encargo copiado tal cual | Hecho | `6071057a`; `docs/encargos/trabajo-laminas-motivos.md`; `contrato.yaml` |
| 2 | Base comprobada con git (b52a760, 5260147, CI 43145636325, ninguna rama, 23.914 bytes) | Hecho | «Base», arriba |
| 3 | 0.1: la tabla de gates, con sus ramas y quién enciende cada hecho | Hecho | §0.1 |
| 4 | 0.2: la rama activa de RN-001 en las láminas 09 y 10 de la sesión 6 de la 7a, con `motor decisiones` y la fila de exposiciones antes | Hecho | §0.2; fila del 2026-11-12. Matiz: las líneas de la bitácora son las de los cortes, 14:09 y 14:23 |
| 5 | 0.3: el recuento contra los HTML | Hecho de otra forma | Los «desconocidos» no están en el HTML: se contaron con la bitácora (§0.3; auditor, fila 28). Desviación aceptada en la respuesta |
| 6 | 0.4: el arreglo con a) a f) y la PARADA | Hecho | §0.4; `63560d14` |
| 7 | Respuesta, punto 0 (RN-008) | Hecho | §0.1 y el comentario de `MOTIVO_GATE["RN-008"]` |
| 8 | Respuesta, punto 1 (contrato con `test_laminas_svg.py`) | Hecho | `contrato.yaml` |
| 9 | Respuesta, punto 2 (recuentos por carpeta) | Hecho | §F2 |
| 10 | Respuesta, punto 3 (recuadro en ADR-0093 §2 y el paso 4) | Hecho | ADR-0093, recuadro del 2026-11-12; PREGUNTAS-7A.md, paso 4 |
| 11 | Respuesta, punto 4 (1.648 px) | Hecho | PREGUNTAS-7A.md, paso 4 |
| 12 | Respuesta, punto 5 (recuadro en `docs/runbooks/LAMINAS.md`, «en su tabla») | **No hecho: PARADA 2** | Ese fichero no tiene la tabla («La respuesta, aplicada punto por punto») |
| 13 | Respuesta, punto 6 (R4.5 en el cierre, comprobada con `problemas_a` a `problemas_d`) | Hecho (propuesta) | PARADA final, línea 2 |
| 14 | F1 (1), (2) y (3) rompen en main, comprobado con `comparar-con-main` | Hecho | §F1, tabla; clon `C:/cmlm/main` |
| 15 | F1: la guardia nueva falla a propósito con la tabla mutada, sin comparar con main | Hecho | `test_la_guardia_falla_si_se_quita_la_frase_de_una_rama` (×4) |
| 16 | F1: «fuera de la ventana» sigue igual | Hecho | `test_fuera_de_la_ventana_sigue_diciendo_fuera_de_la_ventana`, que pasa en main y en la rama |
| 17 | F1: el test de frases cubre las nuevas, sin ninguna sin revisar en silencio | Hecho | 48 → 80 cadenas; una tabla sin cadenas falla |
| 18 | F2: la fila antes, el ensayo en un clon y la v2 en el orden de `clave.txt`; v1 frente a v2 | Hecho | §F2: 42 idénticos, 2 con una línea quitada |
| 19 | F3: la carpeta v2 en todas las líneas que la nombran, y el texto del paso 4 | Hecho | PREGUNTAS-7A.md:49 y :68 (`grep`: solo esas dos) |
| 20 | Qué no cambia: el motor, la spec, los parámetros, el arnés y `motor decisiones` | Hecho | `git diff --stat main...HEAD`, abajo: ningún fichero de `engine/` salvo `laminas.py`, nada de `knowledge/` |
| 21 | Las láminas, byte a byte iguales salvo las frases de causa | Hecho | §F2 |
| 22 | Informe sin fechas ni la clave | Hecho, con un matiz | Ningún día de las láminas ni la clave; sí lleva fechas de calendario de la propia rama (las filas de exposiciones, la respuesta del consultor y el recuadro del ADR), como los informes anteriores |
| 23 | El revisor, con los cuatro alcances más el del recuadro de ADR-0093 | Hecho | Apéndice B |
| 24 | Sin CI de Linux | Hecho | No toca la plataforma: solo `engine/laminas.py`, tests y documentos |
| 25 | La PARADA final con la ruta de la v2 y las líneas de cierre | Hecho | abajo |
| 26 | PROJECT_STATE no crece | Hecho | 23.914 bytes en main y 23.916 en la rama (+2, de la apertura: «Current Feature» nombra la rama); 2008 → 2017 tests, con el mismo número de bytes; la F del cierre no cambia |
| 27 | Seguir sin parar salvo en tres condiciones | Hecho | No se dio ninguna: v2 cambia solo las dos líneas previstas, ninguna foto dio `LaminaError` y ninguna guardia negó nada legítimo (abajo, «Negativas») |

**Desviaciones declaradas**:
- **«Nunca dos causas con el mismo motivo» vale para toda la lista**, no solo para las ramas de
  hecho. Así, un gate que prohíbe los dos efectos (`abrir_operacion` y `buscar_entradas`) ya no
  sale dos veces con «No abre». En las 38 láminas de la 7a eso no cambia nada: ninguna llevaba
  «No abre».
- **El test viejo `test_rn020_dice_del_dia_solo_si_la_rama_semanal_no_puede_disparar` cambia su
  foto** (§F1).
- **Los tests de F1 llevan las frases literales**, para que en main rompan por la frase (§F1).
- **Una causa cierta puede callarse (revisor, b1).** Con `detenido_por_tope` encendido, las ramas
  de predicado no se miran (`_motivos`). Si RN-029 encendió el hecho y después se cumple también
  el acumulador de RN-020, la lámina solo dice el freno de la cuenta: la causa del trader, cierta,
  no sale. Pasa porque `f.origen` se queda con la primera regla, ya que las dos fijan el mismo
  valor (`laminas.py:321-323`; spec:2116 y :2427). No es una causa falsa, que es lo que pide el
  objetivo, pero se aparta de la letra de c), «una frase por rama». En la 7a no pasa (0.3).
- **El test de frases cubre también `CRITERIO_TOMA`, `LADO_ORDEN` y `CIERRE_ANTES`**, que ya
  faltaban en main (revisor, a4).

**Lo que no cambió y se ve**: la línea de frenos «Ya ha gastado sus intentos en esta liquidez:
espera otra liquidez de M15.» (`FRASE_DETENIDO`) sigue en las láminas 09 y 10, junto a la causa
«Iba a colocar la orden y no la coloca: ya ha gastado sus intentos en esta liquidez.». Ya estaba así
en la v1 y el encargo no lo pide.

## Negativas de la guardia

Ninguna negó una medida legítima. Varias negaron comandos compuestos (`git add` seguido de un
ejecutable, `sed` seguido de `state check`, `git show` seguido de `pytest`, un `read` en un bucle,
un `$'\r'`) y un guion con `sys.path.insert` calculado. Se ejecutaron como dice su propio mensaje,
en llamadas sueltas o con la ruta literal, sin rodear nada. Aparte, la comprobación de seguridad de
Claude Code (no la guardia de la casa) negó el `rmdir` de la carpeta vacía `C:\cmlm` de los clones:
se queda, y la quita Aleks.

## PARADA final

**Las láminas de la 7a, v2**: `C:\Users\USER\Desktop\laminas-sesion-7a-v2\`. Son seis carpetas y
38 láminas, en el mismo orden y con el mismo `clave.txt` que la v1; la clave la guarda Aleks y no
va en el ZIP. Cambian solo `sesion-06/lamina-09.html` y `sesion-06/lamina-10.html`: pierden la línea
«…está fuera de la ventana de la sesión.».

**Lo que no me convence:**
1. **Una foto que el motor puede dar y la lámina niega** (revisor, a1, y la corrección de §0.4).
   Puede pasar que RN-004 abra un escenario en el mismo cierre en que RN-016 o RN-001 dispararon
   por `detenido_por_cartuchos`, y que ese cierre sea el corte de una lámina. Entonces
   `motor laminas` da `LaminaError` y no escribe ninguna lámina. Es negar por defecto (decisión b),
   no una frase falsa, y en la 7a no pasó. Pero las láminas de la 7b las genera la activación de la
   7a, y si les toca, esa rama tendrá que decidir. Arreglarlo de verdad pide que la foto guarde los
   hechos del principio del evento, o que el intérprete registre la rama que dispara: las dos cosas
   tocan el motor, que esta rama no podía tocar.
2. **b1**: con `detenido_por_tope` encendido por una regla, la otra causa de tope, si también se
   cumple, se calla (en las desviaciones, arriba).

**PARADA 2**, que no detiene la entrega:

0. **El recuadro del punto 5.** Va en `docs/runbooks/LAMINAS.md` «en su tabla», pero ese fichero no
   tiene tabla de causas. La que da a RN-001 la frase vieja es la del informe cerrado
   `docs/validation/LAMINAS.md` (:108 y :139). Opciones:
   - (a) el recuadro de corrección en `docs/validation/LAMINAS.md`, junto a su tabla de :108 (cuerpo
     intacto, con fecha y rama: CLAUDE.md, «Regímenes de cambio»), ampliando el contrato a ese
     fichero;
   - (b) una nota en `docs/runbooks/LAMINAS.md` (:58-59, donde dice «una causa sin frase en la
     tabla cerrada: error») que remita a LAMINAS-MOTIVOS.md y nombre los `LaminaError` nuevos
     (revisor, b3);
   - (c) las dos.

   Recomiendo (a): es donde está la frase falsa, y la regla de los informes cerrados lo pide. Coste
   de (b) sola: LAMINAS.md sigue diciendo sin aviso una frase que el código ya no da. El error de
   origen es mío: la PARADA decía «LAMINAS.md» sin la ruta. Es una rama corta: un recuadro y un
   `make check`.

**Las líneas de cierre** (para el commit del contrato del cierre, `RITUAL.md`; en la rama no se
tocan):

1. **F**: no cambia. Ya dice «las láminas del bot (LAMINAS.md; `motor laminas`; R4.5) están
   hechas» y «las láminas de la 7a fuera del repo», sin nombrar la carpeta. PROJECT_STATE no crece.
2. **R4.5**, «Estado»: «HECHA (trabajo/laminas, LAMINAS.md). Sus frases de causa, corregidas antes
   de grabar la 7a: la de cada gate sale de la rama que dispara (trabajo/laminas-motivos,
   LAMINAS-MOTIVOS.md).» (196 bytes; antes 50). Comprobada sobre una copia en memoria de la hoja
   con `problemas_a` a `problemas_d` de `tests/unit/test_hoja_de_ruta.py` (guion de la carpeta de
   trabajo, que no escribe nada): `[]` en los cuatro, antes y después.
3. **La fila de ERRORES-RECURRENTES**:
   - **Del consultor**, con su texto del encargo. Importa: las frases de RN-001, RN-020 y RN-029
     nombraban un caso de un gate de varias ramas, y los gates dudosos salían como ciertos. No lo
     vieron el revisor de trabajo/laminas ni la revisión de la v5. Lección para el revisor: cada
     frase de una tabla cerrada se contrasta con la forma entera de su regla y con quién enciende
     cada hecho. Menor: el precedente de la F en el cierre de F38x; lección: un precedente que se
     cita en una orden se lee antes.
   - **De la sesión**:
     - (a) La PARADA nombró «LAMINAS.md» sin ruta, y la respuesta lo aplicó al fichero que no era
       (PARADA 2). Lección: en una PARADA, toda ruta entera.
     - (b) En la PARADA cité la frase de ADR-0093 como §3, y estaba en §2.
     - (c) Un comentario del test de frases daba «39» sin medirlo; medido en el clon de main salió
       48, y se corrigió antes del commit. Lección: una cifra en un comentario también se mide.
     - (d) Del revisor (Apéndice B): en el eje (a), 0 bloquea, 3 importa y 2 menor; en el (b),
       0 bloquea, 2 importa y 1 menor. Lo más útil, a1: el informe justificaba que un hecho sigue
       en la foto con un bloqueo que la spec no da (`abrir_escenario` no tiene `efecto`). Lección:
       un «X lo bloquea» se comprueba en la declaración de la acción, no en lo que prohíbe el gate.
       Y a2: el informe citaba por filas un informe del auditor que no llevaba pegado.
4. **Siguiente tag**: `stable/F38y-laminas-motivos`.

## Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | Recuadro de CORRECCIÓN junto al pasaje de §0.4, sin tocar el texto. El riesgo, en «Lo que no me convence», punto 1. El código no cambia: ya negaba por defecto. El recuadro corrige también que el contrato no protege `cableado.py` |
| a2 | importa | El informe del auditor, pegado tal cual como Apéndice A |
| a3 | menor | Se resuelve con el Apéndice B, pegado abajo |
| a4 | menor | `CRITERIO_TOMA`, `LADO_ORDEN` y `CIERRE_ANTES` entran en los prefijos de `test_ninguna_frase_lleva_ids_dinero_ni_fechas`, que pasa |
| b1 | importa | Declarado en las desviaciones y en «Lo que no me convence», punto 2. No se cambia: hoy no se puede saber con la foto si la rama de acumulador de la otra regla también se cumple, y decir «quizás» sería inventar. Lo decide el consultor |
| b2 | importa | Es la PARADA 2: espera la respuesta del consultor |
| b3 | menor | Entra en la opción (b) de la PARADA 2 |

Lo que el revisor no pudo comprobar y sí está medido en la rama:
- los tests de F1 con el código de main (§F1, el clon `C:/cmlm/main`);
- el recuento de 48 de 70 (el guion repite el filtro de main en ese clon);
- la simulación de R4.5, con `[]` en los cuatro sentidos (guion de la carpeta de trabajo).

Que las filas de exposiciones se escribieran antes de lanzar lo dice el orden de este informe; los
commits no lo pueden probar, porque la fila de F2 se commiteó con el commit de F2.

## Estado

LISTA PARA REVISIÓN: fase 0 respondida; F1, F2 y F3 hechos sin ninguna PARADA condicional; el
revisor pasó (Apéndice B) y sus hallazgos están corregidos o declarados; la PARADA 2 (punto 5)
queda abierta para el consultor; sin CI de Linux, porque no toca la plataforma.

Rama lista para revisión, NO cerrada.

## Apéndice A · El informe del auditor del encargo (fase 0), tal cual

## Auditoria del encargo · trabajo/laminas-motivos · 2026-11-11
Resumen: 39 afirmaciones: 25 correctas, 1 incorrecta y 13 con matiz. Hay 3 herencias no recogidas.

Solo he leído el repo. No he abierto nada fuera de él: ni `laminas-sesion-7a` ni `clave.txt`. No he ejecutado ningún comando de `botsito`, ni con `--help`, y no he escrito nada.

### Afirmaciones
| # | Afirmación (literal del encargo) | Veredicto | Evidencia |
|---|---|---|---|
| 1 | «main y origin/main en b52a760» | CORRECTA | `git rev-parse main origin/main`: los dos dan b52a7602… |
| 2 | «commit de estado sobre el merge 5260147 del tag stable/F38x-preparacion-sesion-7» | CORRECTA | `git rev-parse "stable/F38x-preparacion-sesion-7^{commit}"` da 52601474…; el log de b52a7602 es «docs(state): … cerrada en main» |
| 3 | «ninguna otra rama» | CORRECTA | `git branch -a`: main, trabajo/laminas-motivos y origin/main |
| 4 | «PROJECT_STATE en 23.914 bytes» | CORRECTA | `git show main:PROJECT_STATE.md \| wc -c` da 23914 |
| 5 | «riesgo medio (engine/laminas.py y sus tests; ni el motor ni la spec)» | CORRECTA | contrato.yaml:2 |
| 6 | «tramo R4» | CORRECTA | contrato.yaml:4 casa con HOJA-DE-RUTA.md:316 |
| 7 | «corrige R4.5 antes de grabar la 7a; F de la Next Action, punto (1)» | MATIZ | El punto (1) de F es «grabar, ingerir y activar la 7a» (PROJECT_STATE.md:28). Esta rama es un requisito previo de (1), no (1). R4.5 está HECHA y sus Refs no llevan NA (HOJA:408-414). La entrada de R4 con NA:F es R4.3 (HOJA:385), y su «Depende de: R4.4 y R4.5» está HECHO (HOJA:405, :414). El adelanto está justificado («antes de grabar la 7a»), pero la hoja no tiene ninguna entrada para este arreglo |
| 8 | «MOTIVO_GATE["RN-001"] = «está fuera de la ventana de la sesión» (laminas.py:569)» | CORRECTA | laminas.py:569 |
| 9 | «la forma de RN-001 (strategy_spec.yaml:896-909) prohíbe con cualquiera_de cuatro ramas» | CORRECTA | strategy_spec.yaml:896-909: ninguno_de en_ventana, detenido_por_tope, detenido_por_tope_total y detenido_por_cartuchos |
| 10 | «La frase nombra un caso, no la condición (patrón 3 de ERRORES-RECURRENTES)» | CORRECTA | ERRORES-RECURRENTES.md:46, patrón (3) |
| 11 | «RN-020 (ramas perdida_dia, perdida_semana y el hecho detenido_por_tope; frase «pérdida máxima del día del trader»)» | MATIZ | Las ramas están bien (spec:2109-2112). Pero la rama semanal no puede salir con la frase: `_motivo` da LaminaError con alcance `semana` o `ambos` (laminas.py:1013-1014). Con `dia`, `acumulador_del_trader` da NO a perdida_semana (primitivas_broker.py:360-362), y el registro vale `dia` (parametros.yaml:1523). Hoy el defecto real de RN-020 es solo la rama del hecho encendido por RN-029 |
| 12 | «RN-029 (ramas perdida_dia_firma y el hecho detenido_por_tope; frase «freno diario de la cuenta»)» | CORRECTA | spec:2418-2423; laminas.py:582 |
| 13 | «detenido_por_tope lo encienden RN-020 y RN-029, así que cada una puede salir con la frase de la otra» | MATIZ | No es «puede»: es siempre. El vocabulario dice `produce: [RN-020, RN-029]` y `consume: [RN-001, RN-020, RN-029]` (spec:732-733), y las dos «lo reescriben en cada evento» (spec:740-741). Con el hecho encendido, las dos disparan por la rama del hecho y entran en f.prohibido. Una de las dos frases es siempre falsa, salvo que se den los dos topes a la vez |
| 14 | «RN-008 es un todos_de cuya frase solo nombra la primera condición: parcial, no falsa» | CORRECTA | spec:1534-1539 (dos ninguno_de); laminas.py:574 |
| 15 | «_sin_orden (laminas.py:1022) pone la frase de _motivo (:1010-1019) a cada gate de f.bloqueos (:1055-1058) sin mirar la rama activa, e ignora el segundo campo del par (g, t)» | CORRECTA | laminas.py:1057 (`for g, _ in gates`) |
| 16 | «que puede ser «desconocido» (:440; interprete.py:136)» | CORRECTA | :136 es el comentario. Lo construye `_quien_prohibe` (interprete.py:370-377), y entra también en el bloqueo «prohibida:» (:282-285) |
| 17 | «La vía de f.prohibido y f.quizas (:1066-1074) usa el mismo _motivo» | CORRECTA | laminas.py:1066-1074. f.quizas ya usa la forma dudosa (:591); lo que comparte con f.prohibido es el defecto de la rama |
| 18 | «Ningún test … lo vio» | CORRECTA | Solo se comprueba el conjunto de claves (test_laminas.py:476-485). Los tests de gates de test_laminas_svg.py (:274-290, :354-364, :373-384) usan gates de una sola rama, o RN-020 sin el hecho |
| 19 | «ni el revisor de trabajo/laminas, ni la revisión de la v5» | CORRECTA | La v5 existe (LAMINAS.md:1118). La fila de ERRORES-RECURRENTES.md:117 no lo recoge |
| 20 | «Lo que entra: laminas.py, sus tests…» / «el motor (engine/ fuera de laminas.py y laminas_svg.py)» | MATIZ | El contrato deja fuera `tests/unit/test_laminas_svg.py` (contrato.yaml:5-16). Ahí viven `foto_base` y los tests de frases de gates que el arreglo puede romper: RN-033 en f.prohibido con sesgo alcista (:276-278) daría LaminaError con la decisión b). `contrato_rama.py` falla con un fichero fuera de `rutas_permitidas` (scripts/contrato_rama.py:8). Además, «fuera de laminas.py y laminas_svg.py» sugiere que laminas_svg.py puede cambiar, y el contrato lo protege (:28) |
| 21 | «como ya hace FRASE_TOPE_POR_REGLA (laminas.py:504-510 y :795-803)», sacándola de f.origen | CORRECTA | laminas.py:505-510 y :795-803. `_origen` solo apunta al cambiar el valor (:314-326) |
| 22 | «la misma forma que FRASE_PROHIBE["desconocido"]» | CORRECTA | laminas.py:591 |
| 23 | «`motor decisiones` con las opciones que tiene (--carpeta en data/, --meses, --bitacora)» | CORRECTA | cli.py:3343-3354; `comprobar_carpeta` exige `<repo>/data/` (decisiones.py:62-76) |
| 24 | «verifícalas con --help» | MATIZ | Aquí ninguna regla prohíbe ejecutar `motor decisiones`, pero la práctica documentada es leer la ayuda en el código (UMBRAL-MAYO.md:11, :216). Las opciones ya están en cli.py:3337-3359; `--help` no hace falta |
| 25 | «la bitácora registra los cambios de hechos, decisiones.py:467-475» | MATIZ | Es cierto, pero `quien = {h: r for r, h, _ in c.evento.fijados}` (:468) guarda una sola regla por hecho. Si RN-020 y RN-029 fijan detenido_por_tope en el mismo cierre, la bitácora nombra solo la última. La lámina guarda las dos (`_origen`, laminas.py:323) |
| 26 | «qué rama de RN-001 está activa a las 14:08 y a las 14:22» | MATIZ | La lámina rotula «Corte: a las {corte}, al cierre de la vela de M1 de las {corte-1}» (laminas_svg.py:533-534). La bitácora rotula cada línea con `c.instante`, que es el corte (decisiones.py:344-346, :354; cableado.py:229). En la bitácora las líneas que buscar son las de 14:09 y 14:23, no las de 14:08 y 14:22. Y solo escribe cambios, así que el estado es el del último cambio anterior |
| 27 | «El día … no se escribe ni en el repo ni en el informe» | MATIZ | `--carpeta` tiene que estar dentro de `<repo>/data/` (decisiones.py:66-72). El fichero se llama `bitacora.DIAGNOSTICO.<día>.txt` (:79-83) y cada línea empieza por la fecha (:354). Git lo ignora, pero queda escrito dentro del árbol del repo |
| 28 | «0.3 … o un gate «desconocido» dicho como cierto (contado contra los HTML; la clave no hace falta)» | INCORRECTA | El HTML no lleva `t`: el bloqueo tiene una sola forma, FRASE_BLOQUEO (laminas.py:593), y el par se tira en :1057. Un gate desconocido de f.bloqueos sale con el mismo texto que uno que dispara, así que no se puede contar en los HTML. Hace falta el motor, es decir, el día. La rama activa de RN-001 o RN-020 tampoco está en el HTML: solo hay indicios, como la cabecera con la sesión o las frases de los frenos |
| 29 | F1 (2): «detenido_por_tope encendido por RN-029 no da la frase de RN-020, y al revés» rompe en main | MATIZ | En main la parte de los frenos ya acierta, porque sale de f.origen (laminas.py:795-803). La frase falsa sale solo si RN-020 está en f.prohibido o f.bloqueos, como pasa en el motor real (fila 13). Si la foto del test no lo pone ahí, el test pasa en main y no prueba nada |
| 30 | «test_ninguna_frase_lleva_ids_dinero_ni_fechas (test_laminas.py:518-530) cubre también las frases nuevas … que no quede ninguna sin revisar en silencio» | MATIZ | La función va de :516 a :534. Hoy ya deja sin revisar en silencio todo MOTIVO_GATE, LIMITE_NO_ENVIO y LADO_TOMA: el filtro `t[:1].isupper() and t.endswith(".")` (:530) los descarta porque empiezan en minúscula y no acaban en punto, aunque los nombra en :521. Un dict dentro de otro dict tampoco se recorre (:523-527). Lo que sí revisa cada byte es `comprobar_texto` en tiempo de ejecución (laminas.py:1103, :1234) |
| 31 | «PREGUNTAS-7A.md … la introducción de §1, hacia :49, y el paso 4, hacia :67-69» | CORRECTA | La carpeta sale solo en :49 y :68 (grep en el repo) |
| 32 | F3: «la siguiente dice cómo acabaron las anteriores («Antes, en esta sesión: …»)» | MATIZ | La frase existe (laminas.py:551, :550). Pero choca en la letra con «Ningún resultado se enseña» de ADR-0093 §3 (adr/0093:51) y de PREGUNTAS-7A.md:69. LAMINAS.md:152 y :156 aprobaron los cierres anteriores al corte, y el texto nuevo dice expresamente que la lámina siguiente enseña el resultado de la orden de la anterior. Conviene que el consultor lo diga con esas dos citas |
| 33 | «menos de 1.624 píxeles de ancho» | MATIZ | ANCHO = 1600 (laminas_svg.py:58) más `body{margin:24px}` (:521). 1.624 cuenta solo el margen izquierdo; con los dos márgenes son 1.648. Que entre el SVG con 1.624 es cierto; no he medido el efecto de la barra vertical |
| 34 | «docs/runbooks/LAMINAS.md si describe las causas» | CORRECTA | Solo :58-59 («una causa sin frase en la tabla cerrada: error») |
| 35 | «Sin CI de Linux (no toca plataforma)» | CORRECTA | RITUAL.md:92-96; el cambio son frases |
| 36 | «PROJECT_STATE no crece» | MATIZ | La rama ya está en 23.916 bytes (`wc -c`, +2) por la apertura (diff estadiado: Current Feature y «Archivo 67») |
| 37 | «en el cierre de trabajo/laminas la F anterior se pasó a HISTORIA, y no fue así» | CORRECTA | HISTORIA.md:16957-16958 («No sale ni entra ninguna letra») y :17230-17231 («F se sustituyó sin pasar a HISTORIA») |
| 38 | Las skills abrir-rama y comparar-con-main | CORRECTA | Existen en `.claude/skills/` |
| 39 | La orden de F2 con `motor laminas --sesiones … --salida …` | CORRECTA | cli.py:3360-3374 (más abajo, en los comandos) |

### Lo que el repo pide y el encargo no recoge
| # | Qué | Dónde lo pide | Evidencia |
|---|---|---|---|
| 1 | No publicar en el informe recuentos por carpeta que dejen deducir la clave. F2 pide «cuántas láminas cambian y en qué carpeta y número» | Dos revisores ya lo cazaron: I1 y N2 de `trabajo/laminas`, y b2 de `trabajo/preparacion-sesion-7` | ERRORES-RECURRENTES.md:117 («los recuentos por carpeta dejaban reconstruir la clave») y :118 (b2). El encargo copiado ya nombra «sesion-06 … de 11:00 a 15:00», y PREGUNTAS-7A.md:51-58 da la hora de cada sesión. Cruzar eso con recuentos por carpeta estrecha la clave |
| 2 | LAMINAS.md es un informe cerrado en main y su tabla da a RN-001 la frase que se cambia. El contrato lo protege y el encargo no dice si lleva recuadro de corrección | CLAUDE.md, «Regímenes de cambio», `docs/validation/` | LAMINAS.md:108 y :139; contrato.yaml:37 |
| 3 | En el cierre, la hoja de ruta: R4.5 está HECHA y ninguna entrada recoge este arreglo. Las «líneas de cierre» de la PARADA final no dicen cómo queda | HOJA-DE-RUTA.md:15-19 y RITUAL.md (se actualiza en el commit del contrato) | HOJA:408-414; contrato.yaml:34 protege la hoja en la rama |

### Comandos del encargo
| # | Comando | Existe y se ejecuta así | Evidencia |
|---|---|---|---|
| 1 | `uv run botsito motor laminas --sesiones <las seis de clave.txt, en su orden> --salida C:\Users\USER\Desktop\laminas-sesion-7a-v2` | Sí. `--sesiones` va como `AAAA-MM-DD:sesión` separadas por comas y es obligatoria. `--salida` es obligatoria y va fuera del repo, inexistente o vacía. En Git Bash la ruta con `\` sin comillas pierde las barras: hay que entrecomillarla o usar `/` | cli.py:3366-3374, :2705-2733 |
| 2 | `motor decisiones` con `--carpeta`, `--meses` y `--bitacora` | Las opciones existen, pero el encargo no escribe el comando tal como se ejecuta (falta `uv run botsito motor decisiones --carpeta data/<x> --bitacora <día> …`; patrón 5). `--carpeta` es obligatoria y va dentro de `data/`. Cada día de `--bitacora` tiene que ser de los meses de `--meses` (o de construcción) | cli.py:3343-3359, :2649-2654 |
| 3 | «verifícalas con --help» | Se lee en cli.py; no hace falta ejecutarlo | UMBRAL-MAYO.md:11, :216 |
| 4 | Las comprobaciones del contrato: `uv run botsito state check`, `uv run python scripts/contrato_rama.py` y `make check > make-check.log 2>&1` | Sí | cli.py:3140-3142; scripts/contrato_rama.py existe |

### Lo que no pude comprobar
- La CI de main sobre b52a760, run 43145636325 success: el `gh run view` lo lanza Aleks. Solo coincide con la nota de memoria del cierre de F38x.
- Lo que dicen las láminas 09 y 10 de sesion-06, sus cortes y la sesión de 11:00 a 15:00: está fuera del repo, y no lo abrí por orden.
- Que la bitácora y la lámina pinten las horas en el mismo huso. La lámina usa `puerta.huso`, que es `reloj.huso_visible` (cli.py:2735-2737, laminas.py:1227). La bitácora usa `c.huso` del cableado. No lo medí.
- Que `motor decisiones --meses <mes del día>` dé en ese día el mismo estado que la corrida de construcción entera de `motor laminas`. Por la cuenta por mes debería (cableado.py:283-284), pero no está medido.
- Cómo sabrá laminas.py la rama activa. El intérprete no la registra: `Evento` no tiene ese campo (interprete.py:116-139) y no hay nada de «rama» ni de `cualquiera_de` salvo la evaluación (:255). Además, el contrato protege interprete.py y decisiones.py. Habrá que deducirla de la foto: `limites` y `corte` para la ventana, y `hechos` y `origen` para los frenos. Las ramas de acumulador (perdida_dia, perdida_dia_firma) no están en la foto. Y con un gate «desconocido» no hay ninguna rama activa: la decisión a) no dice qué frase lleva entonces la forma dudosa de d).
- Si el encendido de detenido_por_tope en un cierre deja `origen = (RN-020, RN-029)`, porque la segunda regla lo reescribe en la pasada siguiente del mismo evento. Hoy eso ya sería un LaminaError (laminas.py:797-798). No lo medí.

### Lo más grave
La fase 0.3 pide contar en los HTML los gates «desconocidos» dichos como ciertos, y eso no se puede: la lámina tira el campo `t` (laminas.py:1057) y un bloqueo desconocido sale con el mismo texto que uno que dispara (FRASE_BLOQUEO, :593). Hace falta correr el motor sobre el día, y con eso la clave, aunque el encargo dice que no. La rama activa tampoco está en el HTML ni la registra el motor (interprete.py:116-139), y el contrato protege interprete.py y decisiones.py, así que la decisión a) tendrá que deducirla de la foto; para un gate desconocido no hay rama, y a) más d) no dicen qué frase lleva.

Otras tres cosas pueden hacer trabajar sobre algo falso o mal acotado:
- **RN-020 y RN-029 salen siempre juntas.** No es que «puedan» cruzarse: las dos consumen y reescriben detenido_por_tope en cada evento (spec:732-741). Con el hecho encendido, las dos frases salen juntas y una es siempre falsa. El test F1 (2) solo rompe en main si pone el gate en f.prohibido (fila 29).
- **El test de frases ya no revisa MOTIVO_GATE.** `test_ninguna_frase_lleva_ids_dinero_ni_fechas`, que el encargo da por guarda, hoy deja fuera en silencio MOTIVO_GATE, LIMITE_NO_ENVIO y LADO_TOMA por su filtro (test_laminas.py:530).
- **Dos huecos en lo que se pide.** El contrato no deja tocar test_laminas_svg.py, donde están `foto_base` y los tests de gates que la decisión b) puede romper. Y F2 pide publicar recuentos «por carpeta y número», que dos revisores ya señalaron porque dejan deducir la clave (ERRORES-RECURRENTES.md:117-118).

Ficheros relevantes:
- C:\Users\USER\Desktop\Bot v3\docs\encargos\trabajo-laminas-motivos.md
- C:\Users\USER\Desktop\Bot v3\contrato.yaml
- C:\Users\USER\Desktop\Bot v3\src\botsito\engine\laminas.py
- C:\Users\USER\Desktop\Bot v3\src\botsito\engine\interprete.py
- C:\Users\USER\Desktop\Bot v3\src\botsito\engine\decisiones.py
- C:\Users\USER\Desktop\Bot v3\knowledge\spec\strategy_spec.yaml
- C:\Users\USER\Desktop\Bot v3\tests\unit\test_laminas.py
- C:\Users\USER\Desktop\Bot v3\tests\unit\test_laminas_svg.py
- C:\Users\USER\Desktop\Bot v3\docs\sesion-7\PREGUNTAS-7A.md
- C:\Users\USER\Desktop\Bot v3\docs\runbooks\ERRORES-RECURRENTES.md

## Apéndice B · El informe del revisor, tal cual

## Informe del revisor · trabajo/laminas-motivos · 2026-11-12

Revisado contra `main` (merge-base `b52a7602`): los commits `6071057a`, `63560d14`, `b735dc2b` y `93f0b7f6`, más el informe `docs/validation/LAMINAS-MOTIVOS.md` tal como está en disco (106 líneas añadidas sin commitear, 1 quitada: la línea de estado «EN CURSO»).

**Resultado:** ningún hallazgo bloquea. Hay 3 que importan en el eje (a) y 2 en el (b). La rama no puede cerrarse mientras siga abierta la PARADA 2 (punto 5 de la respuesta del consultor).

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 3 importa, 2 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | **El informe dice algo que su fuente no sostiene.** En LAMINAS-MOTIVOS.md:113-115 afirma: «[los hechos se apagan] con `abrir_escenario`, que RN-001 bloquea porque prohíbe `buscar_entradas`. Por eso un hecho que disparó un gate en el evento sigue en la foto». No es así: `abrir_escenario` no declara `efecto`, y el intérprete solo bloquea las acciones que lo declaran. Por tanto RN-004 puede apagar `detenido_por_cartuchos` en el mismo evento en que RN-001 o RN-016 ya dispararon por ese hecho: los gates van antes, cada regla dispara una vez por evento y la prohibición se mantiene. En ese caso la foto sale sin el hecho y la lámina da `LaminaError` (laminas.py:1130-1131 o :1139-1141). No da una frase falsa, y en la 7a no pasó. Lo que falla es el argumento del informe, no la seguridad del código. | strategy_spec.yaml:471-481: `abrir_escenario` solo trae `argumentos`, sin `efecto`. Grep `^    efecto:` en la spec: una sola coincidencia, `efecto: abrir_operacion` (:448, la de `colocar_orden_limite`). interprete.py:281-291: solo bloquea si `efecto and efecto in evento.prohibidos`. zonas.py:281-282: abrir escenario «apaga `detenido_por_cartuchos`». interprete.py:33 y :338-365: primero los gates, en pasadas, y cada regla una vez por evento. |
| a2 | importa | **El informe del auditor no está en el informe de la rama, pero se cita por filas.** Se citan las filas 7, 13, 20, 26, 28, 29, 30, 32, 33 y 36 sin que el lector tenga dónde comprobarlas. La skill pide «El encargo frente al repo» *con el informe del auditor*, y el precedente es pegarlo como Apéndice A. | LAMINAS-MOTIVOS.md:71, :92, :153, :166-186. `.claude/skills/fase-cero/SKILL.md:101-102`. El precedente: `docs/validation/PREPARACION-SESION-7.md:789` («Apéndice A · El informe del auditor del encargo … tal cual»). `grep -n "Apéndice"` en LAMINAS-MOTIVOS.md: solo :414 y :490, los dos con «Apéndice B». |
| a3 | menor | **«Hecho» antes de que exista.** La fila 23 de «El encargo, punto por punto» marca el revisor como hecho, con evidencia «Apéndice B», y la línea de cierre 3(d) remite al mismo apéndice. En disco ese apéndice aún no existe. | LAMINAS-MOTIVOS.md:414 y :490. |
| a4 | menor | **El docstring del test de frases promete más de lo que el test hace.** Dice: «Cada cadena de cada tabla de frases… nada queda sin revisar en silencio». Pero `CRITERIO_TOMA`, `LADO_ORDEN` y `CIERRE_ANTES`, trozos de texto que salen en la lámina («en el stop», «a mercado»…), quedan fuera de los prefijos. Ya estaban en `main`; no es una regresión. | laminas.py:521, :541, :550. tests/unit/test_laminas.py, `prefijos = ("FRASE_", "MOTIVO_GATE", "MOTIVO_POR_ORIGEN", "LIMITE_NO_ENVIO", "LADO_TOMA")`. |

Comprobado sin hallazgos:
- **El contrato:**
  - `contrato_rama.py`: «CONTRATO: 11 ficheros dentro del contrato…», exit 0.
  - `state check`: OK, exit 0.
  - `make check`: no lo ejecuté. `make-check.log` dice «3443 passed», «SELLO: make check en verde sobre el arbol d68bcd28…» y «PICO DE MEMORIA … 313 MiB». `d68bcd28` es el árbol de HEAD `93f0b7f6` (`git rev-parse 93f0b7f6^{tree}`).
  - El informe de la rama tiene cambios sin commitear: commitearlo pide un `make check` nuevo.
- **Trailer `Fuente:`:** no aplica; ningún commit toca `knowledge/spec` ni `knowledge/cases`.
- **Holdout y material:**
  - Ningún fichero de `knowledge/`.
  - Hay tres filas nuevas en HOLDOUT-EXPOSICIONES: lectura de `clave.txt` y de los HTML, la bitácora, y F2. La de 2026-11-11 está escrita el día 12, desviación aceptada por el consultor.
  - Ningún fotograma ni transcripción.
- **Regímenes de cambio:** HISTORIA (+172/-0), HOLDOUT-EXPOSICIONES (+3/-0) y ADR-0093 (+7/-0) solo añaden líneas (`git diff --numstat`). No hay evidence, feedback, manifests ni corpus.
- **Ambigüedades y guardias de `cita`:** no se tocan ni ambigüedades ni la spec.
- **ADR-0093:** `## Estado` = `ACTIVE`, y `test_adr.py` pasa.
- **Informes cerrados:** ninguno de `docs/validation/` cambia, salvo el registro de exposiciones, que solo añade.
- **Cifras:** `laminas.py` no mete ningún número de negocio nuevo.
- **Clones y repo:** `git worktree list` da solo el repo; no hay ramas nuevas; `C:/cmlm` está vacía, como se declara.
- **Citas del informe que comprobé y sostienen lo que dicen:** interprete.py:183-202 (un hecho da SI o NO); spec:732-741 (RN-020 y RN-029 reescriben `detenido_por_tope`); laminas_svg.py:58 y :521 (ancho 1600 y margen de 24 px); zonas.py:571-576 junto con `parametros.yaml:698` (RN-008 no dispara); laminas.py:1425-1432 (`escribir`).
- **Tests:** `test_laminas_svg.py`, `test_laminas.py`, `test_laminas_registro.py` y `test_adr.py` dan «79 passed». PROJECT_STATE pasa de 2008 a 2017 tests: son 9 funciones nuevas, contadas en el diff. Ocupa 23.916 bytes (`main`: 23.914).

### Eje (b) · Encargo
Resumen: 0 bloquea, 2 importa, 1 menor. Requisitos: 32 hechos, 1 de otra forma (declarado), 1 parcial, 1 no hecho.

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Abrir con abrir-rama, riesgo medio, encargo tal cual | Hecho | `6071057a`; contrato.yaml:2 |
| 2 | Base comprobada | Hecho | merge-base = `b52a7602…`; informe :7-13 |
| 3 | 0.1: tabla de gates | Hecho | 15 filas, comparadas una a una con las formas de la spec (alcance 1, abajo) |
| 4 | 0.2: rama activa de RN-001 a 14:08/14:22 | Hecho (no verificable por mí) | informe :63-84; la bitácora está en `data/` |
| 5 | Fila de exposiciones antes de 0.2 | Hecho | fila del 2026-11-12, en `63560d14` |
| 6 | 0.3: recuento contra los HTML | Hecho de otra forma (declarado y aceptado) | Grep de la v1: 11 RN-009, 3 RN-005, 2 RN-016 y 2 RN-001, en 11 láminas; «No abre»: 0. Cuadra con :88-90 |
| 7 | 0.4: a) a f) y PARADA | Hecho | informe :106-162 |
| 8 | Respuesta 0 (RN-008) | Hecho | comentario en laminas.py, `MOTIVO_GATE["RN-008"]`; 0.1 :45 |
| 9 | Respuesta 1 (contrato y test_laminas_svg) | Hecho | contrato.yaml:9 |
| 10 | Respuesta 2 (recuentos publicados) | Hecho | informe :371-383 |
| 11 | Respuesta 3 (recuadro en ADR-0093 §2 y remisión desde el paso 4) | Hecho | alcance 5, abajo; PREGUNTAS-7A.md:69-70; contrato.yaml:10 |
| 12 | Respuesta 4 (1.648 px) | Hecho | PREGUNTAS-7A.md, paso 4 |
| 13 | Respuesta 5 (recuadro en `docs/runbooks/LAMINAS.md`, «en su tabla») | **No hecho: PARADA 2** | ver b2 |
| 14 | Respuesta 6 (R4.5 en el cierre) | Hecho (propuesta) | informe :472-476; `problemas_a`-`problemas_d` no verificados por mí |
| 15 | F1 (1): cartuchos más RN-001 no dice «ventana», rompe en main | Hecho | test_laminas_svg.py, `test_con_los_intentos_gastados_rn001_no_dice_fuera_de_la_ventana`; alcance 2 |
| 16 | F1 (2): RN-020 y RN-029 no cruzan frases, rompe en main | Hecho | `test_el_tope_de_una_regla_no_sale_con_la_frase_de_la_otra` (×2) |
| 17 | F1 (3): un desconocido no sale como cierto, rompe en main | Hecho | `test_un_gate_desconocido_no_sale_como_causa_cierta` |
| 18 | F1: la guardia falla con la tabla mutada | Hecho | `test_la_guardia_falla_si_se_quita_la_frase_de_una_rama` (×4) |
| 19 | F1: fuera de la ventana sigue igual | Hecho | `test_fuera_de_la_ventana_sigue_diciendo_fuera_de_la_ventana` |
| 20 | F1: el test de frases cubre las frases nuevas | Hecho | test_laminas.py, aserción `len(textos) >= 80` (con la salvedad a4) |
| 21 | F2: fila antes | Hecho | fila del 2026-11-12 de F2; el «antes» no es verificable (ver «Lo que no pude comprobar») |
| 22 | F2: ensayo en un clon | Hecho (declarado) | informe :357-364 |
| 23 | F2: v2 en el orden de `clave.txt`, y comparación | Hecho | alcance 3 |
| 24 | F2: solo cambian frases de causa | Hecho | alcance 3 |
| 25 | F3: carpeta v2 en todas las líneas que la nombran | Hecho | `grep -n laminas-sesion-7a` en PREGUNTAS-7A.md: solo :49 y :68, las dos con `-v2` |
| 26 | F3: texto del paso 4 | Hecho | literal del encargo, con 1.648 en vez de 1.624 (respuesta, punto 4) |
| 27 | No cambian el motor, la spec, los parámetros, el arnés ni `motor decisiones` | Hecho | `git diff --name-status main...HEAD`: de `engine/` solo `laminas.py`; nada de `knowledge/` |
| 28 | Informe sin fechas de las láminas ni la clave | Hecho | grep de fechas: solo 2026-11-11 y 2026-11-12, que son de la rama |
| 29 | Revisor con 4+1 alcances, y su informe pegado | Parcial | este informe; el Apéndice B está por pegar |
| 30 | Sin CI de Linux | Hecho | no toca la plataforma |
| 31 | PARADA final con la ruta de v2 y las líneas de cierre | Hecho | informe :443-491 |
| 32 | PROJECT_STATE no crece | Hecho | 23.916 frente a 23.914; los +2 son de la apertura, declarados |
| 33 | «El encargo, punto por punto» | Hecho | informe :388-418 |
| 34 | Respuesta copiada tal cual en el encargo y en el informe | Hecho | `diff` de encargo:55-69 contra informe:250-264 → exit 0 |
| 35 | Fila de ERRORES-RECURRENTES en las líneas de cierre | Hecho (propuesta) | informe :477-490 |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | importa | **La decisión c) («una frase por rama activa») no se cumple en un caso, y el informe no lo dice.** Supongamos que una de RN-020/RN-029 encendió `detenido_por_tope` y después se cumple también la rama de acumulador de la otra. La lámina solo dice la frase de quien encendió el hecho: la otra causa, que también es cierta, se calla. No es una causa falsa; es una causa cierta que se omite. El informe solo dice «Su frase sale siempre del origen de ese hecho» (:116-118), no esta consecuencia. Hoy no aparece en ninguna lámina (0.3). | Las ramas de predicado solo se miran si no hay ningún hecho activo, salvo la ventana de RN-001 (laminas.py:1132-1152, en concreto :1134 y :1139). `f.origen` solo se fija cuando el valor del hecho cambia (laminas.py:321-323). RN-020 y RN-029 fijan el mismo valor, `hasta_el_corte_siguiente` (spec:2116 y :2427), así que el origen se queda con la primera. |
| b2 | importa | **Punto 5 de la respuesta sin aplicar; la PARADA 2 sigue abierta.** El motivo está bien medido: `docs/runbooks/LAMINAS.md` no tiene tabla de causas ni nombra RN-001, y la frase vieja está en el informe cerrado `docs/validation/LAMINAS.md`. Está declarado como pide la skill (fase-cero, paso 2: PARADA nueva si lo medido contradice la decisión). Mientras no responda el consultor, la rama no se puede cerrar. | `grep -n "RN-0\|ventana\|causa\|tabla"` en el runbook: ningún RN- ni tabla de causas (solo :48, :58-59, :60-64). `grep` en `docs/validation/LAMINAS.md`: :108 `\| RN-001 \| «está fuera de la ventana de la sesión» \|` y :139. Informe :282-288 y :450-465. |
| b3 | menor | **El runbook no recoge los errores nuevos.** «Qué niega» solo dice «una causa sin frase en la tabla cerrada: error». No menciona los `LaminaError` nuevos: rama no identificable, hecho sin origen conocido, regla que dispara sin su hecho, tipo sin frase. El encargo dejaba tocarlo «si describe las causas». Encaja con la opción (b) de la PARADA 2. | docs/runbooks/LAMINAS.md:57-59; las nuevas causas de error en laminas.py:1100-1155 y :1207-1208 |

**Los cinco alcances del consultor**

1. **La tabla de 0.1 y la tabla por ramas, contra la spec**
   - **Tabla de 0.1:** cada fila cuadra con la forma de su regla en la spec: RN-001 (:896-909), RN-037, RN-033, RN-005, RN-008, RN-009, RN-016, RN-018, RN-020, RN-036, RN-022, RN-026, RN-029, RN-031 y RN-032.
   - **Quién enciende cada hecho:** son exactamente cinco `fijar` sobre `detenido_*`: :1912 (RN-016), :2116 (RN-020), :2179 (RN-036), :2427 (RN-029) y :2532 (RN-031). `abrir_escenario` apaga `detenido_por_cartuchos` (:477). Coincide con el inventario de 0.1.
   - **El matiz de la fila 13** («una de las dos frases sale falsa siempre») se sostiene en spec:740-741.
   - **Tabla del código:**
     - `MOTIVO_GATE` tiene las mismas ramas que cada forma, en el mismo orden, y las ramas que son hecho de detención no llevan frase. Lo verifica `test_las_ramas_de_cada_gate_son_las_de_su_forma`, que pasa.
     - `HECHO_QUE_FIJA` y `MOTIVO_POR_ORIGEN` son exactamente esas cinco reglas (`test_quien_fija…`, que pasa).
   - **Si cada frase cubre su rama:**
     - La frase de la ventana de RN-001 solo sale si el corte cae fuera de toda sesión (`fuera_de_ventana`).
     - La frase de cada hecho sale de `f.origen`, nunca del nombre del hecho.
     - La rama semanal de RN-020 está protegida por `_del_trader`.
     - RN-008 es parcial, aceptado en el punto 0.
   - **Lo que no cuadra:** b1 y a1.
2. **Que los tests de F1 rompan en main.** No los ejecuté con el código de `main`: crear el clon escribe en `.git`, y mi papel es solo leer. Lo sustituye la lectura del código de `main` (líneas `-` del diff):
   - `_sin_orden` hacía `for g, _ in gates` y tiraba el `t`, y `MOTIVO_GATE["RN-001"]` era «está fuera de la ventana de la sesión». Así, el test (1) cae en `assert not [… VENTANA …]`, el (2) en `assert not [… no_dice …]` (salen las dos frases), y el (3) en `assert _bloquea(ruido) not in` (sale como cierta).
   - El test de «fuera de la ventana», con la tabla de `main`, da la misma frase, así que pasa.
   - Los tests usan frases literales y `foto_base` está en el propio fichero de test, así que en `main` rompen por la frase y no por un `ImportError`.
   - La guardia con la tabla mutada (×4) da `LaminaError` por la comprobación de laminas.py:1121-1122; `match="sin frase"`.
   - En la rama pasan todos (79 passed).
3. **La v2 solo cambia frases de causa.**
   - Las dos carpetas tienen 44 ficheros cada una, sin `clave.txt`. Los dos `clave.txt` tienen el mismo sha256 (prefijo `cf378ad2b7ff557e`; no los imprimí).
   - `diff -rq --exclude=clave.txt` marca solo `sesion-06/lamina-09.html` y `sesion-06/lamina-10.html`. En cada una, `diff` da una sola línea quitada: `<li>Iba a colocar la orden y no la coloca: está fuera de la ventana de la sesión.</li>` (1010d1009 y 1072d1071).
   - En la v2: 16 causas de gate, 0 «no puede descartar» y 0 láminas con «fuera de la ventana».
   - La frase de intentos sigue saliendo dos veces en la 09 (la del freno y la causa de RN-016), pero el informe lo declara (:429-432) y el consultor solo permitía quitar la línea de RN-001.
   - No usé el guion de la sesión. Lo leí: no imprime la clave.
4. **Ninguna frase nueva lleva ids, dinero ni fechas.**
   - La única cadena nueva es `FRASE_BLOQUEO["desconocido"]`. Las de `MOTIVO_GATE` y `MOTIVO_POR_ORIGEN` son las frases que ya existían.
   - El test reescrito pasa los 80 textos o más por `RE_FECHA` y `RE_PROHIBIDO`, y pasa.
   - Grep en los HTML de la v2: 0 ficheros con `RN-\d`, `ADR-`, `ev-v`, `fb-20`, `USD`, `EUR` o `€`, y 0 fechas `AAAA-MM-DD`.
   - Salvedad: a4.
5. **El recuadro de ADR-0093 §2 dice lo del punto 3, sin añadir ni quitar.** Comparé el texto del recuadro (ADR-0093:59-64, quitando `>` y la cabecera) con el «Su texto: «…»» del encargo:62: `True`, 412 caracteres cada uno. Lo único añadido es la cabecera fechada, con la forma de los recuadros de ADR-0084 (:58, :98).

### Lo que no pude comprobar
- **Ejecutar los tests de F1 contra `main` en un clon** (`git worktree add`): escribe en `.git`. Lo sustituye la lectura estática del alcance 2.
- **El recuento «48 de 70» de `main` y el exacto «80» de la rama.** La guardia negó el `python -c` que importaba `tests.unit.test_laminas` («nombra la carpeta data»), y no lo rodeé. Que son 80 o más lo sostiene la aserción del test, que pasa.
- **La bitácora de 0.2 y 0.3** (`data/laminas-motivos/bitacora`) y la hora de los cortes: está en `data/`, con fechas, y depende de `clave.txt`, que no se abre.
- **Que las filas de exposiciones de 0.2 y de F2 se escribieran antes de lanzar.** La de F2 entró en `93f0b7f6`, después de la corrida; el «antes» solo lo dice el texto.
- **El ensayo de F2 en el clon y sus cifras** (465 s, 644 MiB, la tupla del recolector): no dejan nada en disco.
- **`problemas_a`-`problemas_d` sobre la R4.5 propuesta:** el guion está fuera del repo.
- **Que el encargo sea copia literal del prompt original:** no tengo el original.

### Comandos ejecutados
1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
2. Read: `docs/encargos/trabajo-laminas-motivos.md`, `contrato.yaml`, `docs/validation/LAMINAS-MOTIVOS.md`
3. `grep -n "RN-0\|ventana\|causa\|tabla\|^|" docs/runbooks/LAMINAS.md`; `grep -n "fuera de la ventana\|RN-001" docs/validation/LAMINAS.md`
4. `uv run python scripts/contrato_rama.py`
5. `uv run botsito state check`
6. `ls -la make-check.log && grep -n "SELLO\|PICO DE MEMORIA\|failed\|passed" make-check.log | tail -8`
7. Un bucle `for` con `git rev-parse` y `git log` (negado por la guardia); después `git rev-parse 6071057a^{tree} 63560d14^{tree} b735dc2b^{tree} 93f0b7f6^{tree}`
8. `git log --format='%h %ci %s' main..HEAD`
9. `git diff main...HEAD -- src/botsito/engine/laminas.py`
10. Grep y Read en la spec: detenido_*, RN-001 (:863-912), hechos (:720-769), `abrir_escenario` (:468-483), RN-004 (:1318-1346), `^    efecto:`, RN-031 y RN-032 (:2519-2588)
11. Grep y Read en el código: laminas.py (origen, limites, `_origen` y `_foto`: :300-449; `_sin_orden`: :1157-1230); interprete.py (:180-204, :274-293, :325-368); zonas.py y primitivas (`abrir_escenario`)
12. `awk … strategy_spec.yaml` (volcado de las formas)
13. `uv run pytest -p no:cacheprovider -q …` (dos veces; un intento con `-rA | grep` negado por la guardia); `uv run pytest -p no:cacheprovider -v … | grep -c PASSED`; `… | grep -v PASSED | tail -15` → 79 passed
14. `git diff main...HEAD -- tests/unit/test_laminas_svg.py`; `git diff main...HEAD -- tests/unit/test_laminas.py`
15. Read: `comparar_v1_v2.py` (en el scratchpad de la sesión)
16. `find … ! -name clave.txt | wc -l` en v1 y v2; `sha256sum` de los dos `clave.txt` | `cut -c1-16`
17. `diff -rq --exclude=clave.txt <v1> <v2>`; `diff` de `lamina-09.html` y de `lamina-10.html`
18. `grep -n "<li>"` en `v2/sesion-06/lamina-09.html`; `sed -n '994,1014p'` del mismo
19. `git diff main...HEAD -- docs/sesion-7/PREGUNTAS-7A.md docs/adr/ PROJECT_STATE.md docs/validation/HOLDOUT-EXPOSICIONES.md`
20. `uv run python -c` (compara el recuadro de ADR-0093 con el punto 3 del encargo) → `True 412 412`
21. `grep -n RECUADRO docs/adr/0084-*.md`; `grep -n "^## " docs/adr/0093-*.md`; Read de ADR-0093:17-91
22. `grep -n laminas-sesion-7a` en PREGUNTAS-7A.md y en `docs`
23. `git log --format='%h%n%B' main..HEAD -- knowledge/spec knowledge/cases`; `git diff --name-status main...HEAD`
24. `git diff … | grep -c "^-[^-]"` y `git diff --numstat` (HISTORIA, exposiciones, ADR)
25. `git diff main...HEAD -- docs/state/HISTORIA.md | head`; `wc -c PROJECT_STATE.md`; `git show main:PROJECT_STATE.md | wc -c`
26. `sed -n '58p;521p' laminas_svg.py`; `sed -n '1420,1440p' laminas.py`
27. Grep de los HTML de la v1 (causas por frase, láminas, «No abre») y de la v2 (causas, «no puede descartar», «ventana», número de HTML)
28. `grep -noE` de fechas en LAMINAS-MOTIVOS.md
29. Grep de «Apéndice» y de filas del auditor en el informe; `ls docs/validation/anexos/`; Grep y Read de `.claude/skills/fase-cero/SKILL.md`; `grep "^## "` de PREPARACION-SESION-7.md
30. `diff <(sed -n '55,69p' encargo) <(sed -n '250,264p' informe)` → exit 0
31. `git worktree list; git branch -a; git stash list; ls -la C:/cmlm`
32. `git diff --numstat HEAD -- docs/validation/LAMINAS-MOTIVOS.md`
33. `git log --format='%h %s' --numstat main..HEAD -- …`; `git log --format='--- %h%n%B' main..HEAD`
34. Grep de las constantes de laminas.py fuera de los prefijos; `git show main:src/botsito/engine/laminas.py | grep …`
35. Grep de `RE_PROHIBIDO`/`RE_FECHA`; `sed` de zonas.py:566-578; Grep y Read de `parametros.yaml` (`orden_limite_nace`, :668-700)
36. `uv run python -c` (dos intentos de contar las cadenas, los dos negados por la guardia: `PYTHONDONTWRITEBYTECODE` y «nombra la carpeta data»; no rodeados)
