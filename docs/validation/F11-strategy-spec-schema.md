# F11 · strategy-spec-schema — INFORME DE VALIDACIÓN

**Estado:** WAITING_FOR_USER_VALIDATION · **Rama:** `feature/F11-strategy-spec-schema` ·
**Fecha:** 2026-09-09 · **Cierre previsto:** tag `stable/F11`

`make check` verde de arriba abajo -los siete pasos, `ruff format --check` incluido-: 606 casos (424 funciones), 4 contratos de capas, mypy strict sobre src y tests,
`state/config/knowledge validate` en verde.

---

## 0. Los tres puntos críticos, cerrados

Antes de dar F11 por terminada se revisaron sus puntos débiles. Tres eran reales:

1. **Nadie comprobaba que la spec dijera lo que cita.** El brief lo pedía y no estaba
   implementado. Al encender la comprobación, **diez de las veinticinco reglas fallaron**: sus
   literales estaban escritos de memoria. Corregidas con el texto real de cada cita, y
   `knowledge validate` lo vigila con el mismo criterio de tokens que ADR-0009 usa con la
   evidencia.
2. **Nada obligaba a subir `spec_version`.** El hash solo decía que el manifiesto estaba al día;
   regenerarlo sin pensar dejaba dos specs distintas diciendo ser la misma. Ahora se compara con
   HEAD y es error.
3. **La guardia de números era sintáctica**: "el stop va al ochenta por ciento" pasaba. Ahora
   también mira números en letras, pero solo con unidad, para no prohibir el español corriente.

Y uno más, encontrado al revisarlos: `apply` dejaba `ambiguedad_id` junto a `CONFIRMED` si un
parámetro venía de `DEFAULT_AMBIGUOUS`, produciendo un fichero que no carga. Abortaba sin
corromper, pero sin salida posible. Arreglado con test.

## 0 bis. La auditoría de cierre (tres agentes, 2026-09-09)

Después de darla por terminada, tres agentes auditaron la rama: código, conocimiento y proceso.
Encontraron **veinte hallazgos reales**. Los que más duelen:

| Hallazgo | Por qué importaba |
|---|---|
| **`make check` NO estaba verde** | `ruff format --check` fallaba en dos ficheros. Yo lo daba por verde porque filtraba la salida con `grep`, y "All checks passed" lo imprime `ruff check`, no el format. La CI se habría puesto roja tras el tag |
| **El `huso` no entraba en el hash de la spec** | cambiar `Etc/GMT-2` por `UTC` mueve la ventana operativa dos horas y el manifiesto seguía diciendo ser la misma versión |
| **`apply` podía no escribir nada y decir `OK`** | con el nombre de un parámetro entrecomillado devolvía el fichero intacto, la validación pasaba (es el mismo fichero) y salía con 0 |
| **`apply` no era idempotente** | `--check` decía "9 cambian" sobre un registro recién aplicado, porque comparaba texto contra valor tipado |
| **El valor se escribía sin escapar** | `C:
uevo` se leía después como `C: uevo`: un valor distinto del que dijo el trader, y el fichero cargaba igual de bien |
| **La aritmética del "freno del día" era falsa** | ver §5 bis |
| **8 de 9 definiciones del glosario decían más que su cita** | y nada lo vigilaba: la verificación de literales solo miraba las reglas |
| **`test_no_business_literals` tenía caracteres backspace** | dos patrones (`Europe/Madrid`, `America/New_York`) no casaban con nada desde una edición anterior: la guardia llevaba rota sin que nadie lo viera |
| **`kit check` llevaba roto desde que F11 pobló el registro** | y `make check` no lo ejecuta |

Todos verificados con su reproducción antes de tocar nada, y todos arreglados con test.

## 0 ter. La auditoría del consultor (2026-09-10), punto a punto

Antes de validar F11 se auditó la rama otra vez, esta vez contra el negocio y no solo contra el
código. Once puntos, tres de ellos encontrados al arreglar los primeros. **Esta tabla se cierra fila
a fila; mientras quede una fila ABIERTO, este informe no está listo para el tag.**

| # | Qué era | Estado |
|---|---|---|
| **P1** | La base del 1:3 se contradecía entre `unidad` de `objetivo_rr` ("múltiplo del riesgo") y RN-015 ("sobre la caja completa"), y "riesgo" tiene dos valores en este registro. Un 25 % de distancia al TP dependía de cuál leyera F18 | **CERRADO** · ADR-0014, `base_calculo_objetivo`, A-18, spec 1.5.0 |
| **P2** | `huso_grafico = Etc/GMT-2` entraba CONFIRMED con una cita que no lo dice, y chocaba con `broker_dst: us`, medido contra la demo. A-14 no contemplaba el calendario del servidor y no listaba `huso_grafico` | **CERRADO** · ADR-0015 |
| **P3** | Tras §5 bis, RN-020 es el único freno del día — pero no definía qué reloj ni a qué hora empieza el día, y `perdida_maxima_semanal` no tenía base | **CERRADO** · ADR-0015 |
| **P4** | La verificación comprobaba `literal ⊆ cita`, nunca `regla ⊆ literal`: RN-026 y RN-027 son decisiones del consultor con citas que no las sostienen | **CERRADO** · ADR-0016 |
| **P5** | El hash no cubría `titulo`, `literal` ni `notas` de las reglas. La corrección de riesgo de §5 bis vivía solo en las `notas` de RN-020, y el `titulo` de RN-020 decía lo contrario que ellas | **CERRADO** · ADR-0016 |
| **P6** | `kit check` con `celebrada=True` degradaba TODA diferencia a AVISO, `particiones.yaml` incluida, e imprimía "OK: se recompone igual" bajo sus propios avisos | **CERRADO** |
| **P7** | `feedback apply` desplazaba comentarios de bloque: dos cabeceras de sección quedaron DENTRO de `anclaje_h4` y `lotaje_base`, diciendo lo contrario del parámetro que las contiene. El hash no puede verlo | **CERRADO** |
| **P8** | `PROJECT_STATE.md` y el §6 de este informe describían F11 con cifras de una versión anterior de la rama | **CERRADO** |
| **P9** | `spec manifest --escribir` reescribía solo la línea `hash:`; `generado_el` no se actualizaba nunca (encontrado al cerrar P1) | **CERRADO** |
| **P10** | MASTER_PLAN daba a F21 el criterio de aceptación `stop = −0,75 R`, pre-sesión: la spec validada dice 0,8, y la R no es la que ese criterio supone (encontrado al cerrar P1) | **CERRADO** |
| **P11** | `spec status` contaba "con valor" y "sin él" como si cubrieran el registro; al aparecer los primeros `DEFAULT_AMBIGUOUS` dejó de sumar el total, y "sin valor" era falso para un default (encontrado al cerrar P2) | **CERRADO** |

### P1 · la base del objetivo (cerrado el 2026-09-10)

Tres sitios decían cosas distintas sobre la misma cifra, y ninguna guardia podía verlo porque
`comprobar_literales` mira la cita, no la coherencia entre la regla y la `unidad` del parámetro que
nombra. La decisión —**el 1:3 se traza sobre la caja completa, con la orden, junto al lotaje**— la
sostiene `ev-v2-003256-0197f4e1` ("el objetivo sigue planteado a 1 a 3 aunque el stop se mueva a
0,75") y la mecánica de colocación: cuando se traza el TP, el stop todavía no se ha movido.

La base **sale de la prosa y pasa a parámetro**, que es lo que ADR-0012 ya había hecho dos veces por
el mismo motivo. Y el RR *realizado* queda escrito: `objetivo_rr / stop_fraccion_caja` = **3,75:1**,
no 3:1. Quien mida fidelidad en F26 no debe leer esa diferencia como una desviación del bot.

La guardia nueva (`test_una_base_de_calculo_no_puede_vivir_en_la_prosa`) **encontró el mismo defecto
en RN-012** en su primera ejecución: nombraba `riesgo_por_operacion` sin nombrar su base. Corregido.

Detalle completo en `docs/adr/0014-base-de-calculo-del-objetivo.md`.

### P7 · `apply` se tragaba el comentario de la sección siguiente (cerrado el 2026-09-10)

El bloque de un parámetro se acumula hasta el `- nombre:` siguiente, así que arrastra la línea en
blanco y los comentarios de cabecera de la sección de detrás. `escribir_cambios` añadía
`estado/valor/fuente` **al final** de ese bloque, o sea debajo de esos comentarios.

Pasó dos veces de verdad y llegó a `main`:

- las cinco líneas de la cabecera del bloque F10 quedaron dentro de `anclaje_h4`, diciendo
  *"pre-poblados en UNKNOWN sin valor"* y *"las horas van sin `huso`"* sobre un parámetro
  CONFIRMED, con valor y con `huso`;
- las dos de la cabecera de la auditoría previa, dentro de `lotaje_base`.

**Ninguna guardia podía verlo**: YAML ignora los comentarios y el hash se calcula sobre la
estructura re-serializada. Habría seguido acumulándose en cada `apply`. Las claves se insertan
ahora tras la última clave real; los dos comentarios están reparados y hay test.

### P6 · `kit check` había dejado de poder denunciar nada (cerrado el 2026-09-10)

El perdón a una sesión ya celebrada se escribió para **todo** el paquete. Pero de los cuatro
ficheros solo tres dependen de las respuestas; `particiones.yaml` sale de los hashes de los casos y
del seed, y es **la prueba de que las particiones se fijaron antes de etiquetar** (ADR-0011).
Reescribirlas después de ver las etiquetas solo producía un AVISO y el comando salía con 0.

Ahora el perdón alcanza únicamente a `cuestionario.yaml`, `ventanas.yaml` y `hoja_trader.md`. Y el
mensaje final deja de decir *"se recompone igual"* justo debajo de tres avisos que dicen que no.

### P2 · el reloj del gráfico se afirmaba y no se había medido (cerrado el 2026-09-10)

`huso_grafico = Etc/GMT-2` entraba **CONFIRMED** citando `fb-…-8384b085`, cuyo literal completo es
*"la vela empieza a las 23, la primera vela de cuatro horas"*: no menciona ningún huso. El UTC+2
salía de las `notas` de ese registro, de una lectura de pantalla.

Y al ir al corpus, **todas las lecturas son de verano**:

- `ev-v3-000136-6160fcea`, el trader: *"yo lo tengo configurado como **utc más 2 que son ahora ya
  madrid**"*. Su propia frase ata el UTC+2 a Madrid, y "ahora" es verano.
- `ev-v6-005830-48b30e48`: el fotograma es del 9 de septiembre y muestra `20:48:30 UTC+2`.
  TradingView etiqueta igual un huso fijo que Madrid mientras el horario de verano esté activo.
- `ev-v6-005810-5cb1ef06`, preguntado justo por esto: *"Es la misma hora [...] Si es una hora más,
  pues sería a las 8, o si es una hora menos, a las 6"*. El propio ítem anota que las dos mitades
  de la frase no dicen lo mismo.

**`Etc/GMT-2` y `Europe/Madrid` son indistinguibles de mayo a octubre y no hay una sola observación
de invierno.** De ahí sale la corrección más incómoda de esta auditoría: **ADR-0012 y el informe de
la sesión afirmaban que "la sesión desmintió Europe/Madrid", y no lo desmintió.**

Encima, el reloj del gráfico y el del servidor son **dos relojes distintos** —`broker_dst: us` y
`broker_offset_base: 120`, medidos contra la demo real, dicen que el del servidor sí cambia— y
nada lo decía en ninguna parte.

`huso_grafico` baja a **`DEFAULT_AMBIGUOUS`** bajo A-14, que se reescribe con las tres opciones y
pasa a listar los cuatro parámetros que cuelgan de ella. El registro de feedback mal apuntado queda
revocado con un `REJECT` que lo supersede.

### P3 · el único freno del día no decía qué es un día (cerrado el 2026-09-10)

Tras la corrección de §5 bis, RN-020 es lo único que acota la jornada. Pero "el saldo inicial del
día" no dice **cuándo empieza el día**, y la ficha de `broker_dst` ya avisaba: *"en verano el reloj
va a GMT+3 y el día de riesgo se desplaza"*. Con 0,4 % de pérdida real por cartucho caben unas
**once pérdidas seguidas** antes de tocar el 4,5 %; en cuenta fondeada, el corte no es un detalle.

Nace `reloj_dia_riesgo` (`prop_firm`, `DEFAULT_AMBIGUOUS` en `servidor`, A-19), que **no se le
pregunta al trader: se verifica en el panel de la cuenta**.

Y al mirar el tope semanal apareció algo mejor: el trader **sí había dado su base** —*"9% de la
cuenta actual."*— y no había parámetro donde guardarla, así que `perdida_maxima_semanal` declaraba
"porcentaje de la cuenta" sin decir de cuál. `base_calculo_perdida_semanal` entra **CONFIRMED** en
`saldo_actual`, y **no es la misma base que la diaria**.

### P4 y P5 · lo que ninguna guardia miraba (cerrados el 2026-09-10)

La verificación comprueba que el `literal` esté en su cita. No comprueba —ni puede, en general— que
la regla no diga **más** que su literal. RN-026 (abstenerse por stops level) y RN-027 (redondear el
lotaje a la baja) son decisiones de ingeniería correctas que **nadie dijo**, presentadas con citas
genéricas del trader.

Lo mecanizable es la señal: una regla construida sobre parámetros cuya `fuente` es `decision` está
decidiendo por su cuenta. Campo `decision` obligatorio en ese caso. **La guardia encontró las dos
en su primera ejecución**, y además RN-020, que acababa de heredar el problema.

Y el hash cubría de cada regla solo los campos ejecutables: la corrección de riesgo de §5 bis vivía
**solo en las `notas` de RN-020** y se podía borrar sin mover `spec_version`, mientras el `titulo`
de esa misma regla decía lo contrario que ellas. Ahora entran `titulo`, `literal`, `notas` y
`decision`, y el título dice lo que la regla hace. Por eso `spec_version` sube a **2.0.0**.

### P9 · `generado_el` nunca se actualizaba (cerrado el 2026-09-10)

`spec manifest --escribir` reescribía solo la línea `hash:` con una regex. El sello de tiempo se
validaba en formato y no lo mantenía nadie, así que desde la segunda regeneración databa una
versión anterior de la spec. Ahora se actualiza con el hash, y si la clave falta el comando falla
en vez de escribir un manifiesto a medias.

---

## 5 bis. Una corrección que cambia una decisión de riesgo

El informe de la sesión y RN-020 afirmaban que **el freno del día son los tres cartuchos** y que
"el peor día son ~1,2 % del saldo", muy por debajo del tope del 4,5 %. Sobre esa aritmética se
decidió que el 4,5 % fuera "solo una referencia".

**No se sostiene con los parámetros escritos.** El contador de cartuchos **no es diario**: se
reinicia con la siguiente liquidez de M15 (`cartuchos_reinicio`, y así lo dijo el trader en v6
2:21:07). Son tres pérdidas **por zona de liquidez**, y nada limita cuántas zonas se desarrollan
entre las 07:00 y las 15:00. Los números sueltos son correctos (0,5 % × 0,8 = 0,4 %; 3 × 0,4 =
1,2 %); lo que falla es el salto de "tres pérdidas" a "un día".

Corregido en la regla y en el informe de la sesión. **El tope porcentual no es una red que nunca se
toca: es el único freno del día que existe**, y conviene que el consultor lo sepa antes de F21.

## 1. Qué hace F11

Convierte lo que el trader dijo el 9 de septiembre en una especificación que el bot puede leer:

| Pieza | Qué es |
|---|---|
| `botsito feedback apply` | la puerta que F09 dejó diferida: lleva los valores del feedback al registro, cada uno con su fuente |
| `knowledge/spec/parametros.yaml` | 52 parámetros: **46 con valor, 6 UNKNOWN a propósito** |
| `knowledge/spec/strategy_spec.yaml` | 27 reglas: 24 vigentes y 3 descartadas, todas con su cita |
| `knowledge/spec/glossary.yaml` | 8 términos, cada uno con su literal verificado |
| `knowledge/spec/spec_manifest.yaml` | `spec_version` 1.5.0 y hash sobre los tres ficheros |
| `botsito spec status` | con qué corre el bot y qué sigue en revisión |
| `botsito spec manifest` | comprueba el hash; `--escribir` lo regenera |

## 2. La decisión que más importa: `apply` no interpreta

Catorce valores de la sesión no encajaban en el registro: `"0,8"` con coma, `"3"` como texto donde
se espera un entero, `"sin limite"` donde se espera un decimal, la frase entera del anclaje.

La salida fácil era que `apply` los tradujera. Eso habría metido en el código **una tabla de
interpretación de las palabras del trader**, sin cita, sin revisión y —lo peor— invisible para
`test_no_business_literals`.

En su lugar, `FeedbackRecord` tiene un campo opcional `valor_canonico` que escribe el consultor en
un registro que supersede al de la sesión, **con el literal del trader intacto**. `apply` lo usa tal
cual y **falla** ante cualquier otra cosa.

En su primer uso real falló nueve veces seguidas, y **cada fallo era un problema de verdad**:

1. tres horas sin huso declarado — sin huso, una hora no dice cuándo ocurre;
2. `instrumento` y `cuenta_objetivo`, cuya categoría prohíbe escribirlos por feedback;
3. dos `"no aplica"` y un `"sin limite"`, que no son números;
4. dos registros vigentes a la vez sobre `stop_proteccion_capital`;
5. y, al convertir a `enum`, seis valores que traían la elección con una coletilla explicativa
   detrás (`"al_romper (cada zona de control completada)"`).

## 3. Lo que la sesión obligó a cambiar en el registro

- **`huso_grafico` = `Etc/GMT-2`**, del que cuelgan las tres horas. Y `huso_operativa` deja de decir
  `Europe/Madrid`: la sesión lo desmintió. **Ojo al signo**: `Etc/GMT-2` es UTC**+**2, y hay un test
  que lo fija afirmando +02:00 en enero y en julio.
- **`cartucho_criterio`** y **`cartuchos_reinicio`**: el trader dijo con claridad que un break even
  no gasta cartucho y que el contador se reinicia con la siguiente liquidez de M15, pero no había
  dónde guardarlo. Sin ellos, el bot leería "3" como tres entradas y con reinicio diario: **operaría
  de menos y volvería tarde**.
- **`base_calculo_riesgo`** (saldo actual) y **`base_calculo_perdida_diaria`** (saldo inicial del
  día): la diferencia se perdía porque ambos declaraban "porcentaje de la cuenta", y es justo como
  mide una cuenta de fondeo.
- **`filtro_spread`** y **`objetivo_extension_activa`**: "no hay tope" es un interruptor apagado, no
  un umbral en cero. Un cero en el tope de spread significaría no operar nunca.
- **`cuenta_objetivo`** (fondeada), **`cuenta_pruebas`** (demo) y **`saldo_inicial_cuenta`**, por
  ADR: la cuenta la decide el consultor.

**Seis parámetros se quedan UNKNOWN a propósito**, cada uno con un registro `REJECT` que explica por
qué: el colchón de spread, los dos de reducción por porcentaje de vela, el tope de spread, la
extensión del objetivo y `stop_proteccion_capital`, que es derivado. `UNKNOWN` significa "leerlo
falla", que es exactamente lo que debe pasar con un número que no existe.

## 4. Las reglas no pueden llevar números

Los campos ejecutables de `strategy_spec.yaml` rechazan cualquier cifra que empiece palabra; `M15`,
`H4` y `liquidez_m15_criterio_toma` pasan, porque son nombres. Así, cambiar el stop de 0,8 a 0,75 se
hace **en un sitio** y la spec no se toca. El campo `literal` sí admite cifras: son las palabras del
trader, y censurarlas sería falsear la cita.

Tres reglas nacen **DESCARTADAS** con su motivo y su cita: no hay colchón de spread separado, no se
baja la protección por porcentaje de vela, y el tercer esquema queda fuera. Una regla descartada con
su porqué vale más que una regla ausente, porque la ausencia no se puede revisar.

Y `knowledge validate` avisa de algo que no es formato: **una regla vigente que nombra un parámetro
UNKNOWN no se puede ejecutar**.

## 5. El hash cubre lo que el bot hace

Sobre los **tres** ficheros, `parametros.yaml` incluido. Si el registro quedara fuera, mover el stop
no cambiaría el hash y el pre-vuelo de la demo (F33) daría verde con una estrategia distinta de la
validada — el fallo exacto que MASTER_PLAN H.2 pide impedir, y hay un test que lo comprueba.

Entran también el **estado** y la **fuente** de cada parámetro: pasar de `DEFAULT_AMBIGUOUS` a
`CONFIRMED` no cambia el valor pero sí lo que la spec afirma, y quien mida fidelidad tiene que poder
distinguirlo.

Se hashea la **estructura re-serializada**, no los bytes: un comentario no cambia la spec. La
guardia ya saltó una vez de verdad, al alinear `huso_operativa`, y obligó a subir la versión.

## 6. Qué está corriendo y qué sigue en revisión

```
spec 2.0.0 · hash 21e69c6f2548…
  24 reglas vigentes, 3 descartadas
  46 parametros confirmados, 2 con un default nuestro, 6 sin valor a proposito (54 en total)

Corriendo con un valor que sigue en revision:
  anclaje_h4                   23:00 Etc/GMT-2          A-14
  base_calculo_objetivo        caja_completa            A-18
  break_even_condicion         tocar                    A-13
  filtro_noticias              no                       A-17
  huso_grafico                 Etc/GMT-2                A-14
  objetivo_rr                  3                        A-18
  reloj_dia_riesgo             servidor                 A-19
  ventana_fin                  15:00 Etc/GMT-2          A-14, A-15
  ventana_inicio               07:00 Etc/GMT-2          A-14, A-15
```

Esta salida es de la auditoría del 2026-09-10; la anterior llevaba tres versiones de retraso y es
lo que P8 corrige. Los **nueve** en revisión, no cinco: `huso_grafico` es la raíz de la que cuelgan
las tres horas y no aparecía, porque A-14 solo listaba `anclaje_h4`.

Siete entran **CONFIRMED**: lo dijo el trader, con minuto y cita, y que estén en revisión se ve
cruzando con las ambigüedades abiertas, no degradando su estado. Los otros dos —`huso_grafico` y
`reloj_dia_riesgo`— son **`DEFAULT_AMBIGUOUS`**, que es distinto: ahí no hay palabra del trader que
citar, hay una elección nuestra (ADR-0015).

## 7. Lo que el usuario debe decidir

1. **Validar F11** para el ritual de cierre (merge + `stable/F11`).
2. **A-15 (Nueva York)**, **A-16 (proveedor de datos)** y **A-17 (noticias)** tienen tu decisión
   tomada y anotada, pero siguen `ABIERTA` en `ambiguedades.yaml`, que solo admite cerrarlas con
   feedback del trader. Hay que decidir si esa asimetría se resuelve permitiendo cerrar una
   ambigüedad por ADR, o si se dejan abiertas hasta poder medirlas.
3. **A-13 y A-14 se miden, no se preguntan**: la primera comparando toque y cuerpo sobre los mismos
   días; la segunda, mirando su gráfico en una fecha de invierno (enero ya está congelado).

## 8. Deuda que F11 deja anotada

- **Las reglas son prosa, no código.** `cuando` y `entonces` son texto en español: nada garantiza
  que el motor de F18–F23 implemente lo que la regla dice. Cerrar eso es el trabajo de F12, y
  conviene no darlo por hecho.
- **`apply` reescribe la única puerta de los valores** editando línea a línea para preservar
  comentarios. Funciona y valida el resultado antes de reemplazar, pero es la pieza más frágil y
  la que más vigilancia merece cuando el fichero crezca.
- **Las cadenas de superseders son largas**: hay parámetros con tres registros encadenados. Se
  comprueba que cada `supersede` exista, no que la cadena sea coherente.
- `knowledge/cases/kit/mapa_parametros.yaml` conserva `temas` y `ambiguedad`; sus `opciones` ya
  bajaron al registro. Queda decidir dónde vive el resto (F13).
- La tabla R-01..R-14 → `fb-…` no se ha escrito: las reglas citan directamente el registro de
  feedback, así que ninguna cita "R-03", pero el informe de la sesión sí lo hace.
- `feedback pending` sigue listando todo lo aplicado; con el registro ya poblado, conviene que
  filtre por lo que falta.
