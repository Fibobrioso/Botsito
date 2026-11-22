# AUDITORIA-2026-11-21 · La auditoría del consultor del 2026-11-21, copiada tal cual

Entregada por Aleks el 2026-11-21 y copiada tal cual (rama `trabajo/activar-sesion-08`, F7.1, con
la decisión 0 de la respuesta del consultor del 2026-11-22). Debajo de la raya, el texto sin tocar
una línea: 30737 bytes, sha256 `6dbd381929ce6f3d7e87b2220ab8eca481c54660b125e2c421d67674c181f8ea` del fichero entregado.

```ids-inexistentes
ADR-0087 — no existe a propósito (el 0087 no se rellena); la auditoría lo nombra en su fila 96
```

---

# Auditoría del proyecto · 2026-11-21

Auditoría de solo lectura sobre `main` en 5ae7c482 (tag `stable/F39i-guardia-enlaces`), hecha por el
consultor con tres auditores independientes sobre el clon público del repositorio:

- **A1**, coherencia del estado: PROJECT_STATE, hoja de ruta, HISTORIA, ERRORES-RECURRENTES,
  ambigüedades, parámetros, extracciones y activaciones.
- **A2**, deuda técnica: las 78 líneas de Technical Debt, una por una, contra el código, y la deuda
  que no está apuntada.
- **A3**, mapa del proyecto para los ingenieros y riesgos para la meta.

Ninguno abrió el holdout, `data/`, transcripciones, fotogramas ni los repartos, ni ejecutó código del
repositorio. Este documento no lleva fechas de días reservados ni resultados de operaciones.

Cada hallazgo dice si **el consultor lo comprobó** después en el repositorio (columna «Verif.»):
**sí** (comprobado), **matiz** (cierto con un matiz), **no** (falso, corregido aquí) o **pendiente**
(sin comprobar por el consultor; se comprueba antes de actuar). Mientras corría, la rama
`trabajo/sesion-08` estaba abierta en la laptop de Aleks; nada de esto la toca.

---

## 1. La decisión para Aleks: la meta de marzo

**El hecho (verificado).** La medida de rentabilidad (R5.6), de la que cuelga todo lo que decide
operaciones en vivo (F29 a F32, el porte de la estrategia a MQL5), depende de que la corrida de
construcción dé «habilita medir: sí» (ADR-0070 punto 5; HOJA-DE-RUTA R5.6, «Depende de»). Esa línea
exige una cobertura de 0,70 y una precisión de 0,60 en toda la construcción. La última medida es
**15,7 % y 13,9 %** (31 parejas sobre 198 operaciones del trader y 223 del bot; faltan unas 108
parejas para 0,70).

**Lo que dice la medida, según A3 (pendiente de comprobar las cifras de ritmo):**

- La corrida diaria de contexto se quedó en torno al 20 % tras activar las sesiones 5 y 6. El salto
  de 3,5 a 15,7 vino de cambiar el camino de la cuenta (una cuenta por mes), no de reglas nuevas.
- El pivote de julio (PIVOTES-SESION-7.yaml) pide al menos 19 parejas y como mucho 33 operaciones de
  más. La línea base era 14 y 39; tras la 7a, 14 y 24, y después 11 y 19. Se cumple uno de los dos
  mínimos, lo que según ADR-0093 §6 pide una sesión más.
- Ritmo: 76 ramas en 7,3 semanas (unas 10 por semana). 43 de fidelidad (20 de ellas, logística de
  sesiones), 11 de plataforma y 22 de guardias y proceso (29 %). Desde RUMBO-2026-11, que pedía dos de
  fidelidad por cada una de infraestructura, van 10 de fidelidad por 6 de otras. Las dos ramas de
  guardias de esta semana (F39h y F39i) las propuso el consultor para aprovechar cuota sobrante:
  cuentan en ese 29 %.
- No hay trayectoria medida que diga cuándo llegaría el 0,70/0,60. Con una hipótesis optimista que
  nunca se ha observado (+5 puntos por vuelta de sesión), sería hacia finales de abril de 2027, y la
  cadena completa (mayo, rentabilidad, porte, F34 con sus tres meses de sombra, F35) terminaría hacia
  noviembre de 2027.
- Aunque hoy se quitara esa puerta, el porte (8 a 12 semanas) más los tres meses fijos de F34 llevan
  F35 a finales de mayo de 2027 como pronto: dentro de agosto, pero no en marzo.

| Tramo | Depende de | Estimación (A3) | ¿Cabe en marzo de 2027? |
|---|---|---|---|
| R4.3 (7b: ingerir, activar, S-22/S-19, corrida y pivote) | el trader | 2–4 semanas, diciembre | Cabe |
| R4.6 (vueltas hasta los mínimos de julio) | R4.3; una sesión por vuelta | 2–5 vueltas, enero–febrero, o pivote | Con riesgo |
| Umbral de ADR-0070 (0,70/0,60) | R4.6 y más reglas | sin trayectoria; optimista, finales de abril | **No** |
| R5.2 (mayo) | el umbral | 1–2 semanas | No (lo hereda) |
| F26 (febrero de 2026, diagnóstico) | R5.2, febrero del trader, comando, kappa | 3–5 semanas en paralelo, más el trader | No |
| R5.6 (rentabilidad) | el umbral; hash; cierres y datos de 2025; F17 | preparativos en paralelo; la medida, 1 semana | No |
| R6a.3–R6a.8 (capa del EA) | la demo | 6–9 semanas, enero–febrero | Cabe |
| F28 + F29–F32 (porte) | R5.6 | 8–12 semanas | No |
| F33 / F34 / F35 | F31, F17 / F32+F33 / F27+F34 | 1–2 / 13 fijas / 1 semana | No |

**Las opciones** (cada una necesitaría su ADR):

1. **Mantener la puerta.** Es lo más sólido y lo que Aleks pidió el 9 de noviembre: avanzar buscando
   lo más sólido, aunque cueste tiempo. Entonces la fecha de marzo deja de ser alcanzable y conviene
   decirlo así, también a los ingenieros.
2. **Desatar R5.6 del 0,70/0,60.** La rentabilidad pre-registrada pasaría a ser la puerta, con la spec
   congelada en una fecha fijada de antemano, y la fidelidad seguiría como herramienta de
   construcción. Es la palanca grande. Coste: si no pasa, se gastan los meses de 2025 reservados para
   medirla. A3 añade un argumento: la precisión sobre libros sin vídeo (enero, abril y agosto) está
   sesgada, porque el trader se saltaba las sesiones de break even (S-14; ADR-0092 §11), y eso puede
   dejar el 0,60 fuera de alcance sea cual sea la calidad del bot (**pendiente** de comprobar).
3. **Decidir en la lectura del pivote tras la 7b** (ADR-0093 §6, ya pre-registrada), con el número
   delante.

**Otras palancas que propone A3:** dejar empezar F29/F30 en paralelo, solo en demo, con la puerta en
F33 con cuenta real y en F35; redefinir «marzo» como bot en demo con F34 en marcha y F35 hacia
junio–julio de 2027; empezar ya F17 (sin él, R5.6 no puede dar «pasa»); y bajar la cuota de ramas de
guardias.

**Recomendación del consultor:** la opción 3, pero escribiendo antes las opciones 1 y 2 en un ADR,
**antes de la corrida (3)**, para decidir con el dato y con las reglas fijadas antes de verlo. Y
F17 en paralelo en cuanto haya una prueba gratuita de FTMO, porque no depende de nada.

---

## 2. Hallazgos, uno por uno

Gravedad: **B** bloquea, **I** importa, **M** menor. Destino: dónde entra al repositorio.

### 2.1 Estado, hoja de ruta y Next Action (A1)

| # | Hallazgo | Verif. | Grav. | Destino |
|---|---|---|---|---|
| E1 | La copia de seguridad de v18 y v19 no está hecha. A.4 tenía como fecha límite «antes de grabar la próxima sesión» y está marcada HECHA; su «Hecho cuando» sigue diciendo «v6 a v10». La 7b ya se grabó. Technical Debt (PS:138) dice «falta v18 y v19». | sí | B (ya vencida) | Aleks sube v18 a v21 a Drive con su SHA256; la orden de cierre de la ingesta reabre A.4 o le da dueño y actualiza la línea 138 con v20 y v21 |
| E2 | A-53 tiene cuatro respuestas «en parte» (sesiones 4, 5 y 6 y un ejemplo en la 7a). En la 7b solo está en §3, «las que no caben». `orden_pendiente_al_abrir_escenario` sigue en `se_mueve`, DEFAULT_AMBIGUOUS, aunque las respuestas apuntan a la opción (b). Nadie la recoge después de la 7b. | sí | I | encargo de la activación de la 7b (decidir si se activa con lo que hay) o próxima sesión (R4.6) |
| E3 | La reentrada de la sesión 6 (S-18): ADR-0083 D1 sigue PROVISIONAL («pasa a la sesión 7») y en la 7b es B-11, en §3. | sí | I | igual que E2 |
| E4 | S-23 (la toma de A-46): el consultor tiene pendiente decidir si hay REOPEN desde la sesión 6; en la 7b es B-10, en §3. | pendiente | I | decisión del consultor en el encargo de la activación de la 7b |
| E5 | test_hoja_de_ruta (d) da por cubiertas E2 a E4 solo porque sus ids están en los Refs de R4.3. R4.6 no las recoge. | matiz | M | orden de cierre: que R4.6 las nombre |
| E6 | A-43: `toma_antes_de_la_ventana` vale `cuenta`, CONFIRMED, y en la 7a el trader dijo que si se mitiga antes de las 7 «no es válido» (ev-v19-012529-685ae24d). Su pregunta (B-13) quedó fuera de las seis de la 7b. La lectura del pivote, que se hace una sola vez, correría con ese valor en tensión. | sí | I | antes de la corrida (3): o un mensaje corto al trader por WhatsApp, o la decisión explícita en el encargo de la activación de la 7b |
| E7 | Quién cierra A-16 no coincide: R4.3 y la deuda del panel de FTMO dicen la activación de la 7b; Known Ambiguities y `resuelve_en` dicen F26; R5.1 y ADR-0096 dicen «sigue ABIERTA con la regla de ADR-0092 §9»; ADR-0092 §10 manda cerrarla en la primera rama que toque spec y pague el panel. El paso (2) de la F no lo nombra. Además, la 7a le añadió la vela de otro color. | sí (estado y `resuelve_en: F26`) | I | encargo de la activación de la 7b, que lo fija |
| E8 | R2.3 (letra Q, la exportación de agosto) depende de A.3, que está HECHA y solo trataba marzo y la fecha de la sesión 5. La espera no tiene entrada viva en el carril de Aleks. Desde ADR-0096, A-56 ya no puntúa en F26 y Q pierde peso. | pendiente | I | orden de cierre: entrada viva en el carril de Aleks, o bajar Q |
| E9 | J: su disparador («la próxima sesión que use la hoja») ya no llega, porque la hoja ya no sale de `kit hoja`; G.2 lo redacta distinto («antes de la próxima sesión que etiquete días»). | sí (texto) | M | orden de cierre: reescribir o cerrar |
| E10 | L: viva desde el Archivo 5 y su motivo cayó («caja_bloque ya no cuelga de ese ítem»). | sí | M | orden de cierre: cerrar |
| E11 | M dice «sin objeto mientras break_even_condicion sea cierre», y A.5 sigue pidiendo «M medida». | sí | M | orden de cierre: alinear A.5 |
| E12 | Fechas fijas de la hoja de ruta: la primera entrada (la prueba gratuita de FTMO) caducó y la segunda repite lo mismo. | sí | M | orden de cierre |
| E13 | La cabecera «AHORA» de la Next Action lleva la fecha del 8 de octubre. | sí | M | orden de cierre |
| E14 | La F numera dos veces el paso «(3)». | sí | M | orden de cierre (al reescribir la F tras la ingesta) |
| E15 | C dice que no va antes de las trazas, las láminas ni la preparación, y las tres están hechas: está libre. | pendiente | M | orden de cierre |
| E16 | G.8: «Quién: la sesión, en la próxima rama de guardia», cuando el código ya está hecho y solo falta el traslado de Aleks. | sí | M | orden de cierre |
| E17 | R4.2 está activada pero no puede pasar a HECHA mientras cite NA:F (regla (b) del test); tiene dos líneas «Estado». G.4 también cita NA:F sin relación con la F. | sí (dos Estado) | M | orden de cierre |
| E18 | D, N e I llevan semanas sin moverse. D es coherente con «sin prisa». N: el calendario de cierres cubre hasta una fecha de octubre ya pasada, aceptable porque se renueva por condición, pero conviene decirlo. I pesa más ahora: el sesgo de las sesiones de enero depende de diciembre (PS:150). | sí (N) | M | orden de cierre (N e I, una frase) |
| E19 | R5.3 (marzo) no tiene letra en la Next Action y no se mueve desde la confirmación del trader. | pendiente | M | hoja de ruta: decidir si espera o tiene dueño |
| E20 | A-35 sigue con `bloqueante: true`, y la descripción de `liquidez_m15_pivote_formado` dice «BLOQUEANTE de RN-004», cuando RN-004 está VIGENTE y el parámetro CONFIRMED. | sí (bloqueante) | M | activación de la 7b |
| E21 | A-13 solo sigue abierta por el margen, pero lista como parámetro `break_even_criterio_ruptura`, ya CONFIRMED. El margen no tiene parámetro: si la 7b da una cifra, hace falta uno nuevo en el registro (ADR-0002). | pendiente | I | activación de la 7b |
| E22 | Seis parámetros CONFIRMED arrastran «PROVISIONAL», «por ahora» o «creo» en su historia (por ejemplo `lote_si_no_cabe`). | pendiente | M | una pasada de limpieza de textos, sin prisa |

**Lo que cuadra (A1, comprobado por A1):** las 2122 funciones de test declaradas coinciden con las
contadas; el Marcador, el merge y el tag coinciden; cada cierre de F39d a F39i tiene su fila en
ERRORES-RECURRENTES; todas las letras vivas están en la hoja de ruta y las muertas solo salen en
entradas HECHAS. Un patrón repetido en ERRORES-RECURRENTES es volver a preguntar lo ya decidido (A-20,
dos veces), que es la otra cara de E2.

### 2.2 Ambigüedades respondidas que siguen ABIERTA

- **Esperan a la 7b:** A-13 (el margen, S-2), A-35 (la pregunta 1, S-1), A-48 (el 0, S-3), A-58 (S-4),
  S-22 (S-5) y S-19 (S-6).
- **No las recoge nadie después de la 7b:** A-53 (E2), A-43 en su segunda parte (E6), la reentrada de
  ADR-0083 D1 (E3) y S-23/A-46 (E4).
- **Son mediciones, no preguntas al trader:** A-16 (E7), A-54 y A-55 (esperan la respuesta de FTMO
  del 19 de noviembre) y A-56 (sin puntuación en F26; depende de Q).

### 2.3 Parámetros sin confirmar (A1)

Nueve DEFAULT_AMBIGUOUS y diez UNKNOWN.

- **Los fija la 7b:** `sesgo_h4_rango_nuevo` (A-58), `liquidez_m15_mecha_que_vuelve` (A-35) y
  `orden_stop_punto` (A-48).
- **Sin sesión prevista:** `orden_pendiente_al_abrir_escenario` (A-53).
- **Dependen de FTMO:** los cuatro `freno_*` (A-54, provisionales de ADR-0067) y `cierre_pendientes`
  (A-55).
- **UNKNOWN a propósito:** `stop_segundo_esquema`, `stop_colchon_spread` y
  `perdida_trader_reinicio_huso`.
- **UNKNOWN sin ninguna ambigüedad que los fije:** `stop_reduccion_*`, `objetivo_extension`,
  `spread_maximo`, `stop_proteccion_capital` y `perdida_trader_dia/semana_usd`. Hay que decidir si
  necesitan ambigüedad, pregunta o nada.

### 2.4 Código y deuda que no está en Technical Debt (A2)

| # | Hallazgo | Verif. | Grav. | Destino |
|---|---|---|---|---|
| C1 | **El visor dice «cuenta diaria» y no lo es.** `motor visor --simular --diagnostico-cuenta-diaria` pasa la validación y pone la etiqueta en el nombre y en el HTML, pero `motor_visor` no pasa `cuenta_diaria` al motor (el arnés sí, cli.py:2438): la página sale con una cuenta por mes. Amplía la línea 100 de Technical Debt. | sí | I (alto) | rama corta: conectar la opción o negarla en el visor; hasta entonces, línea de Technical Debt con dueño |
| C2 | `cableado.py:716`: «la fase, si no se pide, es la primera que declara el perfil (DECISION pendiente de validar)». Nadie la sigue. | sí | M | Technical Debt, o decidirlo en la rama de R5.6 (la fase fondeada) |
| C3 | Tres `skip` que ya no pueden saltar: tests/contract/test_golden_citas_f07.py:51, tests/unit/test_simulador_config.py:79 y tests/unit/test_inventario.py:175. | sí (los dos últimos con su texto; el primero, en tests/contract) | M | una rama de limpieza |
| C4 | Más de 15 tests que dependen de `data/` se saltan siempre en la CI de Linux y solo los cubre el make check local (regresión de la cuenta del 7 de agosto, break even, huecos del motor, sesgo del rango, preparar_a35, selector de orden stop, visor, simulación, fidelidad de marzo). | pendiente | M (I para los ingenieros) | página de entrada de los ingenieros |
| C5 | Siete guiones de `scripts/` que nada usa fuera de los informes: caja_77_exploratoria, f35_resultado_r, instante_ticks, repeticion_trader, sesgo_h4_diagnostico, ticks_integridad y verificacion_a35_a44. Son reproducciones sin test y se pudren como el anexo dia_del_bot.py. Ninguno lee libros ni el holdout por nombre. | sí (0 referencias en código, Makefile, tests, skills, runbooks y plan) | M | decidir: moverlos a anexos o declararlos como no mantenidos |
| C6 | `libros.yaml:15` dice «NO ESTAN enero ni septiembre», y enero está (:54). | sí | M | **no se edita** (fichero de solo añadir, ADR-0039): se anota en Technical Debt o con una línea nueva de comentario si el régimen lo admite |
| C7 | Deuda que solo vive en la hoja de ruta (G.1 y G.2): `--diagnostico-a47` y `--diagnostico-a27` siguen en la CLI con A-47 RESUELTA y A-27 DECIDIDA; el token `ambiguo` sin productor; hoja_preguntas.py desfasado; el anexo dia_del_bot.py; los residuos de enlaces. | pendiente | M | ya tienen dueño en la hoja; nada que hacer salvo no perderlos |
| C8 | El docstring de `engine/primitivas.py` dice «Hoy son pocas, y todo lo demas es NO_IMPLEMENTADA»; puede estar desfasado. | pendiente | M | rama que toque primitivas |
| C9 | No hay ningún TODO, FIXME ni XXX en src/, scripts/, .claude/hooks/ ni mql5/. El único xfail es strict y está motivado (línea 84 de Technical Debt). | — | — | — |

### 2.5 La deuda técnica de PROJECT_STATE, línea por línea (A2)

Ninguna línea está pagada del todo. De las 78, **38 no tienen ningún dueño** y otras 12 lo tienen solo
condicional o genérico. Las de riesgo alto:

| PS | Deuda | Verif. | Dueño hoy | Propuesta |
|---|---|---|---|---|
| 97–98 | RN-019 no dispara nunca: `zonas.py:414-416` siempre crea la zona con PRIMER_ESQUEMA y no hay acción `reentrar` en el motor. Falsea la medida de fidelidad, que la re-corrida ya cuenta como «error nuestro conocido». | sí (PRIMER_ESQUEMA fijo) | ninguno | dueño en R4.6 o rama de motor propia, ligada a la reentrada (E3) |
| 100 | El visor sin cuenta diaria (y C1). | sí | ninguno | C1 |
| 111 | Un fotograma dentro de un tramo no citable se puede abrir con Read por su ruta: la guardia no tiene regla para `data/fotogramas/`. Es la única fuga de contenido protegido por Read que sigue abierta. | sí (la guardia solo lo nombra en un mensaje) | ninguno | rama corta del carril de guardias, junto con la 109 |
| 102 | 32 ids exactos de casos ocultos fuera de `knowledge/cases`. | (medido en F39h) | G.7 | ya tiene dueño |
| 130–131 | Una pregunta abre N particiones (`paquete.py:1369-1373`) y el fallback de `leer_fichero` (`holdout.py:331`). | pendiente | NA:G | rama corta de kappa antes de cualquier autorización (ADR-0096 §4) |
| 159 | El día quemado de holdout-2 no está en retirados.yaml. | no medible sin la puerta | la rama que use holdout-2 | se queda |
| 138 | La copia de seguridad (E1). | sí | ninguno vivo | E1 |

Riesgo medio: 82, 85, 89, 91, 92, 94, 95, 99, 101, 105, 106, 107, 109, 116, 117, 118, 122, 125,
134–135, 142, 143, 150, 156 y 157. Las de riesgo bajo, el resto. La tabla completa, con la
comprobación de cada línea, está en el anexo A.

**Correcciones de texto que pide A2:** la 86 cita :46 y es :45; la 100 cita cli.py:2558 y hoy es hacia
:2539; la 92 es parcial (`getattr(os/sys…)` ya se trata como no decidible; node y perl siguen); la 124
es dudosa (`universo()` ya separa los dos caminos): medirla y, si procede, sacarla; la 119 y la 123 no
son deuda (una es un límite de git aceptado, la otra un hallazgo de investigación): reclasificarlas.

**Cuidado con PROJECT_STATE:** está en 24.576 bytes de 25.000. Cada línea nueva (C1, C2…) tiene que
salir de otra o ir a HISTORIA; las correcciones de E9 a E18 deberían liberar bytes.

---

## 3. Lo que cada uno hace, en orden

**Aleks**
1. Copia de seguridad en Drive de v18, v19, v20 y v21 (vídeos, audios, crudas, filtradas,
   transcripciones y fotogramas) con su SHA256SUMS, en cuanto termine la ingesta (E1). La lista exacta
   la deja el informe de la ingesta.
2. Decidir el camino de la meta (§1), con calma, antes de la corrida (3).
3. Cuando haya una prueba gratuita de FTMO, F17 (el grabador de deslizamiento): no depende de nada.
4. Decir si `rescate` y `video-mapeo`, que ya no están en el Escritorio, se borraron o se movieron, y
   si `rescate` estaba en Drive.

**Orden de cierre de la ingesta (`trabajo/sesion-08`)**, en su commit del contrato, sin pasar de 25.000
bytes: E1 (A.4 y la línea 138 con v20 y v21), E5, E8 a E18, la línea de C1 en Technical Debt con
dueño, y las correcciones de texto de §2.5. Este documento entra en el repositorio antes, en un commit
propio de la rama siguiente, como `docs/validation/AUDITORIA-2026-11-21.md` (el `chore(cierre)` no
admite ficheros nuevos).

**Encargo de la activación de la 7b:** E2, E3, E4, E6 (antes de la corrida (3)), E7 (A-16 y el panel
de FTMO), E20 y E21. Y el ADR de las opciones de §1, si Aleks lo quiere antes de la corrida.

**Carril de guardias, cuando toque:** la 111 con la 109; luego G.7.

**Ramas cortas sin fecha:** C1 (el visor), RN-019 (97–98), kappa (130, 118 y 131), C3 y C5.

**Página de entrada de los ingenieros:** el anexo B, más C4.

---

## 4. Lo que los auditores dijeron mal

- A3 dijo que el índice de ADR (`docs/adr/README.md`) no lista el 0037: **es falso**, está en la
  línea 101.
- A3 dijo que la fila de F30 en MASTER_PLAN «contradice» a ADR-0092 §7: **matiz**. La NOTA del
  2026-11-19 de MASTER_PLAN (ADR-0096) dice expresamente que es la actualización que ADR-0092 encargaba
  y que ninguna fila cambia. La fila sigue nombrando F26, pero la nota de cabecera manda.
- A2 situó el skip de test_golden_citas_f07.py en tests/unit; está en tests/contract.

---

## Anexo A · Technical Debt, línea por línea (A2)

| PS | Deuda | ¿Verdad hoy? | Dueño | Riesgo |
|---|---|---|---|---|
| 82 | meses_reservados sin salida | Sí (holdout.py:652-720, solo añadir) | R5.4 / NA:I | medio |
| 83 | validador del journal en mql5bridge | Sí | F23 (condicional) | bajo |
| 84 | guardia: `//` y literal de separadores | Sí (xfail strict) | G.1 genérico | bajo |
| 85 | el bróker reserva margen por pendiente | Sí | R6a.6 | medio |
| 86 | docstrings de viabilidad_* | Sí (línea :45, no :46) | difuso | bajo |
| 87 | LF de UltimaLinea redundante | Sí | ninguno | bajo |
| 88 | globales del EA tras cambio de símbolo | Sí (solo test textual) | ninguno | bajo |
| 89 | herramientas fuera del matcher (publish_files) | Sí | G.1 genérico | medio |
| 90 | riesgo residual de guardia-g1 §4.3 | Sí | G.1 | bajo |
| 91 | riesgo de C (rutas compuestas) | Sí | NA:D / G.1 | medio |
| 92 | riesgo de B (node, perl, getattr) | Parcial | NA:D / G.1 | medio |
| 93 | guiones de plataforma sueltos | Sí | procedimiento con «!» | bajo |
| 94 | excepción de carga por ruta (endswith) | Sí | G.1 | medio |
| 95 | ADR-0088: git status y fd | Sí | G.1 | medio |
| 96 | ADR-0087 en ids-inexistentes | Sí | sin fecha | bajo |
| 97 | RN-019 no dispara nunca | Sí | **ninguno** | **alto** |
| 98 | la nota de RN-019 cita A-31 | Sí | ninguno | bajo |
| 99 | zona reutilizada ligada al escenario viejo | Sí | regla del trader | medio |
| 100 | visor sin cuenta diaria (y C1) | Sí, y peor | **ninguno** | **alto** |
| 101 | curva_con_deslizamiento arrastra `previo` | Sí | F17 | medio |
| 102 | ids de casos ocultos fuera de su sitio | — | G.7 | alto |
| 103 | VISOR-DIAS.md incompleto | Sí | ninguno | bajo |
| 104 | el visor no enseña las H4 saltadas | Sí | ninguno | bajo |
| 105 | test_visor y test_preparar_a35 leen marzo | Sí (declarado) | ninguno | medio |
| 106 | `--hasta` no recorta las H4 de contexto ni el resumen del bróker | Sí | ninguno | medio |
| 107 | dias_de_mercado sin línea LECTURA | Sí | G.2 | medio |
| 108 | docstring de freno.py | Sí | R6a.4 | bajo |
| 109 | Read de crudas sin cuarentena | Sí | carril de guardias | medio |
| 110 | ffmpeg -ss/-t | Sí | ninguno | bajo |
| 111 | PNG de fotograma en tramo no citable | Sí | **ninguno** | **alto** |
| 113 | ingesta con el reloj del registro | Sí (condicional) | disparador | bajo |
| 114 | sin git callan anclas y spec_version | Sí | ninguno | bajo |
| 115 | RN-029 a RN-032 con cita de relleno | Sí | R6a.4 | bajo |
| 116 | ADR-0042 §2 por nombre | Sí | ninguno | medio |
| 117 | spread por hora de pared | Sí | ninguno | medio |
| 118 | gramática del kit por operación | Sí | rama de kappa (NA:G) | medio |
| 119 | cherry-pick y rebase sin puerta | Sí (límite de git) | aceptado | bajo (reclasificar) |
| 120 | v5_criterio solo ventas | Sí | ninguno | bajo |
| 121 | cuerpo de informe cerrado | Sí | ninguno | bajo |
| 122 | Oanda frente a Dukascopy | Sí | activación de la 7b | medio |
| 123 | fractal 5/120 | hallazgo, no deuda | — | bajo (reclasificar) |
| 124 | guardia de cobertura en universo() | Dudosa | heredado 7 | bajo |
| 125 | no_trade por ausencia | Sí | ninguno | medio |
| 126 | fecha_grabacion sin uso | Sí | ninguno | bajo |
| 127 | buscar en el corpus antes de una ambigüedad | Sí (condición vencida) | ninguno | bajo |
| 128 | lector guardado para cases/<camino>/ | Sí | disparador | bajo |
| 129 | lectura_de_velas lee el config de hoy | Sí | ninguno | bajo |
| 130 | una pregunta abre N particiones | Sí | rama de kappa (NA:G) | alto |
| 131 | fallback de leer_fichero | Sí | rama de medida de F26 | alto |
| 132 | token sin productor | Sí | ninguno | bajo |
| 133 | pregunta con instante sin ítem | Sí | ninguno | bajo |
| 134–135 | el detector no ve temas hermanos | Sí | ninguno | medio |
| 136 | propuesta sin supersede | Sí | ninguno | bajo |
| 137 | CONFIRM sobre un ítem supersedido | Sí | ninguno | bajo |
| 138 | copia de seguridad: faltan v18 y v19 | Sí | **ninguno vivo** | medio (vencida) |
| 139 | alias de la raíz: OSError | Sí (atenuado) | G.1 | bajo |
| 140 | cotizaciones sin tick | Sí | sin dueño | bajo |
| 141 | panel de FTMO: textos viejos | Sí | activación de la 7b | bajo |
| 142 | zona de RN-005 en el escenario anterior | Sí | regla del trader | medio |
| 143 | `motor decisiones` sin lote ni stop | Sí | ninguno | medio |
| 144 | toca_colocar_orden_limite con estado | Sí | ninguno | bajo |
| 145 | láminas sin esquema | Sí | ninguno | bajo |
| 146 | dos textos que ADR-0093 deja viejos | Sí | ninguno | bajo |
| 147 | CLI de láminas sin test entero | Sí | ninguno | bajo |
| 148 | guardia: barra dentro de una cadena | Sí | G.1 (fix/) | bajo |
| 149 | feedback pending (RN-003) | Sí | G.2 | bajo |
| 150 | sesgo de enero según el arranque | Sí | diciembre (NA:I) | medio |
| 151 | texto del sesgo del visor sin test | Sí | ninguno | bajo |
| 152 | anexos sin lint | Sí | ninguno | bajo |
| 153 | test_guardia_falsos_positivos inestable | Sí (no reproducido) | ninguno | bajo |
| 154 | la lámina calla la segunda causa | Sí | ninguno | bajo |
| 155 | LaminaError en RN-004 | Sí | ninguno | bajo |
| 156 | la CI se cuelga instalando ffmpeg | Sí (sin caché ni timeout de paso) | ninguno | medio |
| 157 | sin comando de medida de F26 | Sí | rama de medida de F26 (NA:G) | medio |
| 158 | septiembre sin entrada en libros.yaml | Sí | rama de septiembre | bajo |
| 159 | día quemado de holdout-2 sin retirar | no medible | rama que use holdout-2 | alto si se olvida |
| 160 | docstring de test_kit.py:706 | Sí | rama que toque test_kit | bajo |

La columna «¿Verdad hoy?» es de A2; el consultor comprobó la 97, la 100, la 111 y la 138.

---

## Anexo B · Mapa del proyecto para los ingenieros (A3)

**Qué es.** Un bot de EURUSD que replica a un trader concreto (sesgo en H4, liquidez en M15, entrada
en M1), construido regla a regla desde lo que el trader dice y hace en vídeo, verificable operación a
operación contra sus backtests, y que tiene que ejecutarse como Expert Advisor de MetaTrader 5 en una
cuenta FTMO 2-Step Swing de 100k. Sin IA en ejecución. Python 3.12 con `uv`; MQL5 para la plataforma.
Tamaño: `src/botsito` unas 40.000 líneas, tests unas 55.000 (2.122 funciones), la guardia 6.000, MQL5
unas 1.700 (ninguna de estrategia todavía). 94 ADR (el 0087 y el 0095 no existen a propósito).

**Conocimiento (`knowledge/`, versionado).** `evidence/` (citas del corpus, inmutables); `feedback/`
(respuestas del trader por sesión, solo se añade); `spec/` (`strategy_spec.yaml` con las reglas RN y
su «forma» sin números, `parametros.yaml` como registro único de cifras, `ambiguedades.yaml`,
glosario y manifiesto con hash); `cases/` (dev legible, holdout PROHIBIDO, fidelidad, vistos, kit,
`criterio_fidelidad.yaml` con los umbrales pre-registrados, meses reservados y retirados); `corpus/`
(`libros.yaml`, solo se añade; manifiestos inmutables; tramos no citables); `cuentas/` (perfil FTMO y
cierres de mercado); `simulador/llenado.yaml`.

**Código (`src/botsito/`), en capas que impone import-linter (ADR-0006):** `domain` (cálculo puro
sobre velas, sin IO ni reloj ni MetaTrader); `data` (velas M1 y ticks de Dukascopy, agregación a H4 y
M15); `config` (la puerta del registro, ADR-0002); `corpus` (transcripción y fotogramas;
`cuarentena.py`, la única fuente de lo que no se enseña); `evidence` y `feedback`; `retrieval`
(`kb find|at`); `spec`; `cases` (ingesta, particiones, la PUERTA del holdout en `holdout.py`, kit,
criterio de fidelidad, kappa); `engine` (el intérprete de la forma con primitivas escritas a mano,
ADR-0030; el motor por día; el bróker, el llenado, la cuenta FTMO y el freno; `cableado.py`; el arnés
que mide fidelidad; el diagnóstico: bitácora, visor y láminas); `mql5bridge` (genera `Generado.mqh` con
su hash, compila y valida el journal); `validation` (`knowledge validate`).

**MQL5.** `mql5/Experts/Botsito.mq5` y `Include/Botsito/Capa/*.mqh`: la capa de ADR-0082, que conecta,
solo funciona en DEMO, lee reloj y sesiones y escribe el journal v2. No decide operaciones.
`tools/mql5/MedirDemoFTMO.mq5` mide la demo.

**Cómo se relaciona todo.** Vídeos y sesiones del trader → corpus → evidencia y feedback → spec.
Backtests del trader → casos (dev; holdout detrás de la puerta). Dukascopy → datos → dominio. Spec y
dominio → motor → simulador → arnés (operaciones del bot contra los casos dev) → criterio de
fidelidad → diagnóstico y láminas → sesión con el trader → feedback. El ciclo actual (ADR-0093):
corrida en julio → diferencias → láminas → sesión (como mucho seis preguntas) → extracción →
activación con un test que rompe → corrida nueva.

**Los ADR imprescindibles.** 0001 (regímenes de cambio), 0002 (registro de parámetros), 0006 (capas),
0013 y 0019 (la spec y su forma), 0030 (intérprete y primitivas), 0021, 0033 y 0037 (holdout y su
puerta), 0048 y 0050 a 0053 (arnés y simulador), 0043 y 0070 (fidelidad y umbral), 0092 y 0096
(fidelidad para construir, rentabilidad para operar), 0082 (arquitectura del EA). Del método: 0093 y
0026.

**Las reglas que un ingeniero rompería sin querer.** El holdout (ni abrir ni listar `holdout/`, ni
libros de meses con días reservados, ni agregados, ni Analytics, ni la carpeta de marzo; febrero no se
descarga; correr el arnés lee el M1 de meses reservados para calentar, y se declara). Los regímenes
(evidencia inmutable, feedback y libros solo se añaden, informes cerrados con recuadro, PROJECT_STATE
solo el presente, HISTORIA solo crece). El trailer `Fuente:`. Las cifras al registro. Los
pre-registros no se tocan sin ADR, y ningún parámetro se ajusta por rentabilidad. `make check` con
salida a un fichero y sello antes de cada commit; nunca `--no-verify`, cherry-pick ni rebase. `main`
no se toca y el cierre solo con orden de Aleks. La guardia no se rodea.

**Cómo se arranca.** `make sync`; `make check > make-check.log 2>&1`; `make rapido`;
`uv run botsito --help`; `uv run botsito motor arnes --simular` (necesita `data/` local). Sin la
máquina de Aleks, el arnés y muchos tests se saltan (C4). La transcripción pide `--group asr`, ffmpeg y
GPU; MQL5 se compila con MetaEditor en Windows.

## Estado

Entregado a Aleks el 2026-11-21. Pendiente de entrar al repositorio en la rama siguiente a
`trabajo/sesion-08`.
