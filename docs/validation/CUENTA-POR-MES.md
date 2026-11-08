# CUENTA-POR-MES · la cuenta del motor, una por mes (ADR-0092 §8)

Rama `trabajo/cuenta-por-mes`, abierta el 2026-11-07 desde `main` 8aeed0b
(tag `stable/F38r-metodo-fidelidad-rentabilidad`, merge a1907fa). Encargo:
`docs/encargos/trabajo-cuenta-por-mes.md`. Tramo «R3 · Una corrida del arnés sobre toda la
construcción» (R3.8 de la hoja de ruta; F de la Next Action).

## 0. La base, comprobada con git al abrir

- `git rev-parse HEAD` en main = `8aeed0b336c0e80ab1d7124096f04880e569ede7`; `origin/main` el mismo
  (`git fetch origin --prune`; `git ls-remote --heads origin` solo da `refs/heads/main`).
- `git rev-parse "stable/F38r-metodo-fidelidad-rentabilidad^{commit}"` =
  `a1907fa3d0dead56bc109cea6f680841c8e629cc` = `git rev-parse main^1`; el tag esta en origin
  (`git ls-remote --tags origin`, objeto 4323f6b).
- `gh run view 42440794180 --json headSha,conclusion,status,workflowName,headBranch`:
  `{"conclusion":"success","headBranch":"main","headSha":"8aeed0b336c0e80ab1d7124096f04880e569ede7","status":"completed","workflowName":"ci"}`.
- `git branch -a`: solo `main` y `origin/main`; `git ls-remote --heads origin "fix/*"` vacio.
- Modelo: Opus 5.5, el que pide el encargo.

## Fase 0 · inventario sin tocar código (2026-11-07)

Medido leyendo el código de la rama recién abierta (idéntico a `main` en `src/`, `scripts/` y
`tests/`) y contrastado por el subagente `auditor-encargo` (53 afirmaciones: 36 cuadran, 14 con
matiz, 3 no cuadran; sus hallazgos, en e) y en la PARADA condicional). Ninguna corrida del arnés.

### a) El estado que `MotorCableado` guarda entre días, y el orden de los días

| Estado | Dónde vive | Dónde se reinicia hoy |
|---|---|---|
| `cuenta` (`CuentaViva`) | `cableado.py:243` | nace en `correr_dia` si es `None` (`:278-279`); con `cuenta_diaria`, a `None` cada día (`:276-277`) |
| `seguidor` (`SeguidorTope`, A-44) | `:244` | nace si hay `tope` y es `None` (`:294-297`); con `cuenta_diaria`, cada día (`:277`) |
| `racha` (`SeguidorRacha`, RN-036) | `:247` | nace si es `None` (`:280-281`); con `cuenta_diaria`, cada día (`:277`) |
| `primero_en_tocar` | `:249` | nunca: `_anotar_toque` vuelve en cuanto tiene valor (`:413-414`), también con `cuenta_diaria` |
| `trazas_broker`, `brokers`, `estados` | `:250-252` | por clave de día; solo salida (los leen el informe y el visor) |

El bróker (`Broker(...)`, `:283`), el `ContextoDia` (`:303`) y el estado de estrategia
(`EstadoDia()`, `:316`) nacen cada día: D1 cuadra en que no hay nada más que reiniciar. El freno de
peticiones vive en el bróker (`reglas_broker.freno` es configuración).

El orden: `arnes.validar_meses` ordena y deduplica los meses (`arnes.py:121`);
`arnes.dias_de_construccion` recorre `for mes in meses` y dentro del mes los casos por id
(`arnes.py:151-172`, `sorted(c ...)` en `:158`); `arnes.correr` es una comprensión plana sobre esos
días (`arnes.py:238`), que no agrupa por sí misma: el agrupado viene de `dias_de_construccion`. Así
un mes nunca queda partido. El visor con `--todos` usa la misma función (`Preparador.dias`,
`visor.py:281-282`) y llama a `correr_dia` día a día (`visor.py:325`). `cli.py` solo ordena la
etiqueta `Corrida.meses`.

### b) Los consumidores y los textos de D7, uno por uno

| Consumidor | Qué lee hoy | Con varias cuentas |
|---|---|---|
| `curva_de_equity` (`cableado.py:561-572`) | `motor.cuenta.cerrar_dia_en_curso()`, filtrada por `trazas_broker` | daría solo la curva del último mes: cada cuenta cerrada guarda la suya (D3) |
| `MotorCableado.veredicto` (`:512-515`) | `motor.cuenta` | el veredicto del último mes; los de los cerrados, en D3 |
| `_primero_en_tocar` (`:749-753`) | `motor.primero_en_tocar` | el del último mes; los demás, en D3 |
| `informe_simulacion` (`:756-828`) | todo lo anterior y `motor.racha` | D4: con un mes igual; con varios, bloques por mes |
| `_informe_metodo` (`:1310-1407`) | `curva_de_equity` y `motor.cuenta.estado` (`:1365-1366`) | D5 |
| el visor (`detalle_para_visor`, `:743-744`; `visor.py:145-146`, `:949-950`) | `TrazaBroker.saldo_fin` y `equity_fin`, por día | no cambia; el primer día de un mes nuevo trae el saldo de la cuenta nueva |
| `scripts/embudo_77.py:905` | rótulo literal «cuenta arrastrada entre dias (ADR-0053 §6)» | deja de ser cierto: se cambia (D7) |
| `scripts/f35_resultado_r.py:81` | rótulo «arrastrada entre dias», sin «cuenta» ni ADR; NO construye el motor: lee el JSON de `embudo_77` (`:70-74`) | se cambia igual, para que describa el JSON que escribe `embudo_77` desde esta rama |
| `scripts/orden_stop_o_limite.py:431`, `scripts/caja_77_exploratoria.py:146` | construyen el motor y corren `arnes.correr` sobre varios meses (`:435`, `:150`); NO llevan ningún rótulo de la cuenta | nada que cambiar en el texto; si se vuelven a correr, sus decisiones entre meses cambian (dentro de un mes, no) |
| `cli.py:2324-2326` | ayuda de `--diagnostico-cuenta-diaria`: «en vez de arrastrarse (ADR-0053 §6)» | se reescribe |
| `diagnostico.py:35-37` | «la corrida normal arrastra la cuenta entre dias (ADR-0053 §6)» | se reescribe |
| comentarios de `MotorCableado` (`cableado.py:240-241`, `:245-246`, `:248`) | «por defecto se arrastra, ADR-0053 §6», «persiste entre dias», «en toda la corrida» | se reescriben. `:139`, `:192` (`MOTIVO_FIN_DIA`, que se imprime) y `:382` citan ADR-0053 §6 por la red de seguridad del fin del día, que sigue cierta: no se tocan |
| `racha.py:1-3` | «PERSISTE entre dias como la cuenta (ADR-0053 §6)» | fuera de las rutas del encargo: PARADA condicional, punto 1 |

### c) Los tests que corren días con el motor cableado

Medido con un espía de `MotorCableado.correr_dia` que anota los meses de cada motor y lanza
`pytest tests/unit` (guion y salida en `anexos/CUENTA-POR-MES/medir_meses.py` y
`meses-fase0.txt`; la primera forma, un plugin por `PYTHONPATH`, la negó la guardia por la
variable de entorno, y se rehízo sin ella): **89 tests corren el motor cableado, 0 motores corren
más de un mes**, y los meses vistos son `2030-01` (los sintéticos) y `2026-04` (un motor de un
solo mes; ningún test de esta rama ni ninguna corrida del arnés). Los que corren VARIOS días en
el mismo motor son todos de enero de 2030: `test_cableado.py:713-723` y `:766-774` (días 15 y 21),
`test_racha_perdidas.py:375-390` (15 a 28) y `test_reinicio_tope_trader.py:190-198` (15 y 16).
Ninguno corre más de un mes: ninguno de los seis de D7 se cambia.

Los que asertan la cabecera: PRIMERO EN TOCAR, `test_preparar_a44.py:371` y `:398`; TOPE, `:349`;
RACHA, `test_racha_perdidas.py:411`; «CUENTA: REINICIADA CADA DIA», `test_cableado.py:778`; la
cabecera y la curva enteras, por el prefijo del golden de e01e28c, `test_metodo_adr0092.py:370-383`
(compara hasta `CABECERA_METODO`: la sección de ADR-0092 no tiene golden).

### d) D1-D8 frente a lo medido

- D1: cuadra para la cuenta, el seguidor del tope y el primero en tocar. **No cuadra para la
  racha** (PARADA condicional, punto 1).
- D2, D3, D4: cuadran. D4: el golden existente cubre la cabecera, la curva y los eventos, no la
  sección de ADR-0092 (la cubre la guardia nueva de D5).
- D5: cuadra, con tres medidas. (i) `perdida_diaria_maxima` y `equity_minima_del_tramo` son un
  máximo y un mínimo POR DÍA (`criterio_fidelidad.py:657-675`), así que por cuenta salen la misma
  cifra que sobre la curva de todos los días seguidos: lo nuevo es decir de qué mes, y no cambia
  ninguna cifra. (ii) La guardia nueva no protege nada con el `_motor` de los tests, que no lleva
  `criterio`: la sección solo dice «sin el criterio de ADR-0092» (`cableado.py:1320-1327`). El
  golden se genera con el criterio REAL (`cargar_criterio`) puesto en el motor, para que salgan a)
  a f), en una carpeta nueva `tests/golden/metodo_adr0092/` (la de `informe_simulacion/` está
  protegida por el contrato). Y (iii) reescribir el motivo de f) sin condición choca con «con un
  solo mes, igual que hoy»: PARADA condicional, punto 2.
- D6: cuadra. D7: cuadra con los matices de b) (los guiones). D8: cuadra; el recuadro de ADR-0070
  punto 3 queda en futuro (PARADA condicional, punto 3).

### e) El encargo frente al repo (auditor-encargo)

Lo que no cuadra o cuadra con matiz, y gana el repo:
1. «los guiones que construyen el motor cableado (embudo_77, f35_resultado_r, orden_stop_o_limite,
   caja_77_exploratoria)»: `f35_resultado_r.py` no lo construye; el rótulo literal solo está en
   `embudo_77.py:905`; los otros dos no llevan rótulo (b).
2. «el bucle de arnes.correr agrupa por mes»: agrupa `dias_de_construccion`; `correr` es plano (a).
3. METODO-FIDELIDAD-RENTABILIDAD.md §0.c cita líneas anteriores a los commits de F38r
   (`cableado.py:219-228` hoy es `:240-249`, `arnes.py:226-234` hoy es `:231-239`).
4. ADR-0049 dice que la cuenta persiste en DOS sitios (`:132`, H6, y `:178`, H6 (c)): la NOTA va
   tras el primero, que es la decisión.
5. «22.764 bytes» cuadra en `main`; en la rama ya son 22.675. El tope del repo es 25.000
   (`tests/unit/test_project_state.py:21`); los 23.000 son el margen de los encargos.
6. La «lección 8 de F38r» está en `docs/runbooks/ERRORES-RECURRENTES.md:112`, trampa (8), no en el
   informe de F38r.
7. Al marcar R3.8 HECHA, su `Refs` pierde `NA:F` (F sigue viva): si no, `test_hoja_de_ruta.py:144-145`
   falla con «esta HECHA y la letra sigue viva». Va en las líneas del cierre.
8. `curva_con_deslizamiento` y `veredicto_con_f17` toman una sola curva y su `previo` se arrastraría
   entre cuentas. Hoy no tienen llamadores (solo los tests); cuando F17 los use, irán por cuenta.
   Anotado como deuda, sin tocarlos.
9. D5 no nombra la tabla de posiciones, el material sin vídeo ni el punto de equilibrio de la
   sección: quedan como hoy, sobre todas las operaciones.

**Lo que se aplica sin esperar**, porque cuadra con lo medido: D1 para la cuenta, el seguidor del
tope y el primero en tocar; D2, D3, D4, D5 (con el golden en carpeta nueva y con el criterio real),
D6, D7 (con los guiones como dice b) y D8. Sigo con la fase 1 sin esperar respuesta, como pide el
encargo.

### PARADA condicional (solo en esto; lo demás se aplica)

1. **La racha de RN-036 al cambiar de mes.** D1 la reinicia, pero la descripción del acumulador en
   la spec dice «contando en TODOS los dias de la corrida … el calendario no la reinicia»
   (`knowledge/spec/strategy_spec.yaml:847-853`, protegido por el encargo), el trader dijo «la
   racha sigue de un día a otro y una semana otra» (`parametros.yaml:1416-1426`) y ADR-0077 §3 la
   ata a la cuenta «PERSISTE entre días como la cuenta» (`:46-49`), igual que `racha.py:1-3`
   (fuera de las rutas). ADR-0092 §8 solo habla de «la cuenta». **Aplicado mientras tanto: la racha
   NO se reinicia al cambiar de mes** (lo de hoy); la cuenta, el seguidor y el primero en tocar,
   sí. **Propuesta:** aplicar D1 entero, porque ADR-0077 §3 la hace vivir «como la cuenta» y en
   vivo la cuenta nunca salta de enero a abril; eso pide, en el mismo commit, una NOTA en ADR-0077
   §3, el texto de `racha_perdidas` en la spec con `botsito spec docs --escribir` y su trailer
   `Fuente: ADR-0092`, y el docstring de `racha.py`, con las tres rutas en el contrato. Es una
   línea en `correr_dia` y un test que ya está escrito (D6 (2), la parte de la racha, marcado
   `xfail` estricto hasta la respuesta).
2. **El motivo de f).** D5 lo reescribe a «alguna cuenta entro en SUSPENDIDA», y D4/D5 piden que
   con un mes todo sea igual que hoy. Con un mes y la cuenta SUSPENDIDA, si N llega al mínimo, la
   línea «criterios a) a f)» cambiaría (el golden sintético no lo ve: N=1 da «insuficiente»).
   **Aplicado:** el motivo dice «la cuenta entro en SUSPENDIDA» con una cuenta y «alguna cuenta
   entro en SUSPENDIDA (AAAA-MM, ...)» con varias. **Propuesta:** dejarlo así; o, si se quiere el
   texto nuevo siempre, es un cambio de una línea y se dice que con un mes cambia.
3. **ADR-0070 punto 3.** Su recuadro y su fila del índice dicen «La implementa
   `trabajo/cuenta-por-mes`», en futuro; D8 solo marca «Implementado» en ADR-0053 y ADR-0070 no está
   en las rutas. **No tocado. Propuesta:** la misma coletilla «Implementado en
   trabajo/cuenta-por-mes (2026-11-07)» al final de su recuadro, en esta rama o en el cierre.

## Fase 1

### Punto 1 · Los textos de D8

- ADR-0092 §8: una NOTA (2026-11-07) con la lista de lo que empieza de nuevo al cambiar de mes, la
  condición, el porqué, la diaria intacta y la medida de §5 sin existir todavía. La racha va en la
  NOTA como PENDIENTE de la PARADA condicional, punto 1: la NOTA dice lo que hace el código.
- `docs/adr/README.md`: la fila de 0092 nombra la NOTA.
- ADR-0053 §6: el recuadro gana al final «Implementado en `trabajo/cuenta-por-mes` (2026-11-07; …)».
- ADR-0050 H6 (§2) y ADR-0049 H6: una NOTA de una línea cada uno, que remite a ADR-0092 §8. En
  ADR-0049 va tras el párrafo de la decisión de H6 (`:132-136`); el resumen de alternativas
  (`:178`) no se toca.
- Ningún cuerpo reescrito. ADR-0070 punto 3, sin tocar (PARADA condicional, punto 3).

## Estado

EN CURSO.
