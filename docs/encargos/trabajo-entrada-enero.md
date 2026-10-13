# Encargo · trabajo/entrada-enero

Dado por Aleks (consultor) el 2026-10-13. Copiado tal cual (hasta que exista, el ADR que el
encargo manda escribir va declarado aquí en un bloque `ids-inexistentes`, como exige
`knowledge validate`; sale del bloque en el commit que lo crea):

```ids-inexistentes
ADR-0079 — el ADR de la fase 3 que este encargo manda escribir (enero entra en construcción); no existe hasta su commit
```

> Modelo: Opus · Esfuerzo: alto
>
> ENCARGO: trabajo/entrada-enero — X (los ticks por la rejilla) y enero de 2026 entra en construcción (R2.2)
>
> BASE
> - Rama nueva trabajo/entrada-enero desde main 6fb483b (tag stable/F37o-entrada-julio, merge a4e4fa6), con la skill abrir-rama: encargo copiado tal cual en docs/encargos/, contrato.yaml y Archivo en HISTORIA. Si la base no cuadra (sha, tag, CI de main 38463152743, otra rama viva), PARA.
>
> OBJETIVO
> Que enero cuente en construcción como julio: scripts/ticks_spread.py cuenta la ventana por la rejilla (NA:X, ADR-0069 §5, heredado 34 parte a), y enero entra con tramo, reparto dev-visto, casos, ADR y ticks de invierno. El precedente es ENTRADA-JULIO.md: el mismo orden de commits (su decisión 5) y los mismos pasos, salvo lo que se dice abajo.
>
> QUÉ NO CAMBIA
> - Ni el motor, ni la spec, ni los umbrales de criterio_fidelidad.yaml: solo la lista construccion, con su ADR.
> - Ni llenado.yaml (el spread supuesto sigue medido sobre abril y agosto, como dejó ADR-0078; decláralo).
> - Ni diciembre, ni ningún mes reservado.
> - No corras el arnés ni midas cobertura ni precisión: eso es R3.1.
>
> DECISIONES DEL CONSULTOR (2026-10-13), que entran en el informe y en el ADR
> 1. Enero es construcción: 0 casos en cualquier partición, fuera de meses_reservados.yaml, en vistos.yaml (visto_el 2026-08-30), libro ya declarado en libros.yaml (UTC, 2026-10-06). Repite las tres medidas en la fase 0.
> 2. Diciembre de 2025 NO se baja en esta rama: es material del trader sin decidir (NA:I) y no está en vistos.yaml, así que un kit build posterior lo sortearía como ciego. Consecuencia que se acepta y se declara: los primeros días de enero calientan el sesgo H4 con pocas velas, como abril antes de tener marzo (MOTOR-SESGO-H4.md). El tramo empieza el 2 de enero, así que el 1 no entra. Mide en la fase 0 qué días de enero quedan afectados y si alguno sale INSUFICIENTE.
> 3. La ADR nueva es la 0079 (verifica que es el siguiente número libre): 2026-01 entra en construccion; ningún umbral cambia; la decisión es anterior a cualquier corrida del arnés con enero.
>
> FASE 0 — inventario, sin abrir nada y sin escribir (skill fase-cero, con el agente auditor-encargo)
> a) La base, y las medidas de la decisión 1, con recuento y sin imprimir ids.
> b) HOLDOUT-EXPOSICIONES: verifica qué declara la fila del 2026-10-06 sobre el libro de enero (según el auditor del consultor, solo dateStart y entryPrice, «ninguna otra columna»). Y verifica que cases/visto.py:102-111 da por cumplida la condición 2 de ADR-0042 §2 solo porque el nombre del fichero aparece en el documento: es un falso positivo. No lo arregles aquí; descríbelo.
> c) ticks_spread.py: cómo cuenta hoy la ventana (huso_operativa con astimezone) y qué ofrece reloj_de_las_sesiones (cases/relojes.py, reexportado en engine/relojes.py) para contarla por la rejilla. Verifica que no hay ningún test suyo. Mira también simulador_config.py, que lee el spread por hora local de llenado.yaml, y di si queda desalineado con la rejilla los días de desfase (ADR-0069 §1).
> d) Los tests que enumeran meses y que romperán: test_criterio_fidelidad.py:108 y test_mes_del_material.py:252 (verifícalo), y los textos que dicen «construcción = abril, julio y agosto» (ADR-0043 y su NOTA, ARNES-MOTOR.md, SESION-DE-PREGUNTAS.md, docs/adr/README.md).
> e) El manifiesto de ticks de julio (horas 05-13 UTC, verano) frente a enero (invierno, 06-14 UTC por la rejilla; verifícalo con reloj_de_las_sesiones, no lo supongas).
> f) La decisión 2 medida: qué días de enero cubren las velas M1 (primera vela 2026-01-01T22:04Z según el auditor), y cuáles quedarían INSUFICIENTE en el sesgo H4 sin diciembre.
> g) PARADA. Copia tal cual en el informe la columna de fechas del libro de enero, leída por Aleks hoy, una sola vez (ADR-0072): mínima 2026-01-02, máxima 2026-01-30 (vio también la hora de esas dos filas, y nada más). Decláralo hoy en HOLDOUT-EXPOSICIONES. Entrega el inventario y espera mi respuesta antes de escribir nada.
>
> FASE 1 — X: ticks_spread.py por la rejilla
> - La ventana sale de reloj_de_las_sesiones (la puerta de ADR-0069 §5), no de astimezone sobre huso_operativa.
> - El script itera todos los meses de construccion, incluidos julio y enero, y exige sus ticks.
> - Un test que rompa a propósito con un día sintético de desfase (por ejemplo, uno del 26 al 30 de octubre): con huso_operativa la hora sale corrida y con la rejilla no; y otro que compruebe que en un día sin desfase dan lo mismo.
> - simulador_config.py no se toca: si la fase 0 confirma el desajuste, se declara y va como propuesta de Technical Debt.
>
> FASE 2 — enero: lectura, tramo y reparto (lo que en julio fue 3.a-e)
> a) Repite casos_reservados y casos_ocultos para 2026-01 en el commit en que lees: 0. Si no, PARA.
> b) Fila nueva en HOLDOUT-EXPOSICIONES, HOY y ANTES de ingerir: la lectura completa del libro de enero (todas las filas y todas las columnas que lee casos ingerir), con el nombre del fichero.
> c) Tramo de 2026-01 en cobertura_material: 2026-01-02 a 2026-01-30, con el material_sha256 del libro (ee4ade46…, cópialo del manifiesto). Es un límite inferior, como abril y julio.
> d) uv run botsito casos visto --mes 2026-01; commit del reparto y su ancla antes de ingerir.
> Commits con Fuente: ADR-0042 (o ADR-0039 / ADR-0072 donde toque), porque ADR-0079 aún no existe.
>
> FASE 3 — ADR-0079, en su propio commit
> - 2026-01 entra en construccion. Actualiza en el mismo commit los dos tests de la fase 0.d y los textos vivos (NOTA en ADR-0043, ARNES-MOTOR.md, SESION-DE-PREGUNTAS.md, el índice de ADRs). Trailer Fuente: ADR-0079.
> - El ADR dice: la decisión 2 (diciembre no, con los días afectados), que llenado.yaml sigue medido sobre abril y agosto, y lo que la fase 1 cambió.
>
> FASE 4 — casos y ticks
> - uv run botsito casos ingerir --material "<ruta del libro de enero>" --fecha <hoy>, y después uv run botsito casos check.
> - uv run botsito data download-ticks --dataset eurusd-ticks-2026-01 --simbolo EURUSD --escala 100000 --desde 2026-01-01 --hasta 2026-01-31 --solo-dias-dev --horas <las de invierno que midió la fase 0.e>. Después uv run botsito data check-ticks --dataset <id> --hashes. Di cuántas horas se perdieron. Si se pierden muchas, se repite antes de commitear, como en abril, agosto y julio.
>
> INFORME docs/validation/ENTRADA-ENERO.md
> - Fase 0 con la PARADA y mi respuesta literal; cada fase con su evidencia; desviaciones declaradas; exposiciones del día.
> - Propuestas para la orden de cierre:
>   - X sale, HECHA, y R2.2 pasa a HECHA;
>   - F apunta a lo siguiente según la hoja de ruta;
>   - I: quita «después de X», que ya estará hecha;
>   - Technical Debt: el falso positivo de visto.py (basename en HOLDOUT-EXPOSICIONES) y, si se confirma, el desajuste de simulador_config.py con la rejilla;
>   - tamaño de PROJECT_STATE, que ya va en 23,3 KB: si una entrada nueva lo acerca al tope, propón qué se condensa.
>
> TESTS Y CI
> - make check > make-check.log 2>&1 antes de cada commit, con su sello. Nunca --no-verify.
> - Si la rama cambia el Makefile o el clasificador niega un push, para y dame el comando con «!».
> - No hace falta fix/ salvo que toques .claude/ o código que dependa de la plataforma; si tocas algo de eso, fix/entrada-enero con su CI de Linux y los números de run.
>
> REVISOR Y ENTREGA
> - Skill entregar-rama, con el revisor y su informe pegado al final del tuyo.
> - Que mire en especial el orden de los commits, la fila de exposición antes de ingerir y el test del día de desfase.
> - Termina con: «Rama lista para revisión, NO cerrada».

## Respuesta del consultor a la PARADA (2026-10-13)

Copiada tal cual:

> Respuesta a la PARADA de trabajo/entrada-enero (consultor, 2026-10-13). Cópiala tal cual en el informe y aplícala punto por punto.
>
> 0. Orden de construccion: aceptado, enero al final: ["2026-04","2026-07","2026-08","2026-01"]. Siete ficheros de tests usan construccion[0] y cinco corren el arnés; así ninguno cambia y el commit del ADR no corre el arnés sobre enero. Que ADR-0079 diga que el orden de la lista importa y por qué.
> 1. test_mes_del_material.py:252: aceptado, en el commit de la fase 2, como en julio. test_criterio_fidelidad.py:108, en la fase 3. Es el orden en que cada uno rompe.
> 2. Ticks de enero con --horas 06-14: aceptado. Es la ventana de la rejilla más una hora, el mismo criterio que abril, julio y agosto, y lo mediste.
> 3. Fase 1: aceptado. ticks_spread.py sigue recorriendo construccion, con su test sintético del día de desfase. La corrida real con los cuatro meses va después de la fase 4, a un anexo, sin tocar llenado.yaml.
> 4. test_huecos_motor correrá el sesgo sobre enero: aceptado y declarado en ADR-0079, como con julio. Lee solo velas; no mide nada.
> 5. NOTAS en ADR-0069 §5 y ADR-0051 DN-5, y corregir VISOR-DIAS.md:9, en el commit de ADR-0079: aceptado. Amplía el contrato a esos tres ficheros. Lo que un commit deja falso se corrige en ese commit.
> 6. Falso positivo de visto.py: aceptado, solo como Technical Debt. Anota que el mecanismo por nombre lo fija ADR-0042 §2, así que arreglarlo pide una NOTA o un ADR nuevo, no solo código. En esta rama, la fila nueva de HOLDOUT-EXPOSICIONES (fase 2.b) es la que cumple de verdad la condición 2.
> 7. simulador_config.py: aceptado como Technical Debt, con la medida (2026-10-27: 4 de 11 horas, 1 punto de spread distinto). Añade a la línea que importará cuando se mida un mes con días de desfase: marzo, del 9 al 27, y octubre.
>
> Además:
> - La lectura de fechas de enero: declara que la sesión ya leyó la columna el 2026-10-06, antes de ADR-0072, y que la de Aleks de hoy es la que fija el tramo según ADR-0072. No es una exposición nueva: enero no tiene ningún día en ninguna partición.
> - Para la orden de cierre, en §8: el heredado 34 frente a R2.2 HECHA, y R5.4 sin NA:X. Propón el texto exacto de los dos cambios para que test_hoja_de_ruta.py pase.
>
> Sigue con la fase 1. Si el Makefile cambia o el clasificador niega un push, para y dame el comando con «!». Al terminar: revisor, y «Rama lista para revisión, NO cerrada».
