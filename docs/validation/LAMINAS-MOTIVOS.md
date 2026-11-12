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

## Estado

EN CURSO: F1, F2 y F3 hechos; queda el revisor y la PARADA final.
