# Encargo · trabajo/demo-ejecucion-1

Dado por Aleks (consultor) el 2026-10-09. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva: trabajo/demo-ejecucion-1, desde el main actual. Antes de abrirla, verifica con git el sha de main y que el último tag de HISTORIA apunta a su merge; si hay otra rama abierta, para y dímelo. Ábrela con la skill abrir-rama: este prompt tal cual en docs/encargos/trabajo-demo-ejecucion-1.md, su contrato.yaml y el archivo en HISTORIA del PROJECT_STATE.md de main.
>
> Contexto (lo declara Aleks, 2026-10-09): ejecución 1 de MedirDemoFTMO en la prueba gratuita del 2026-10-08, lanzada a las 07:35 de Lima (14:35 de España, después de las 07:30 que se evitaban). Terminó «completo» en unos 45 segundos, sin órdenes ni posiciones abiertas al final y con el balance en 99.999,75 USD. El fichero está en data/demo_ftmo/MedirDemoFTMO_20261009_153552.csv, copiado tal cual y sin abrir con Excel. Es la ejecución 1 de 3; las 2 y 3 van en la segunda prueba, desde el 26-10.
>
> Objetivo: punto A de la Next Action, «con el primer CSV, rama para fijar los valores de ADR-0057 y A-27», más lo que esta medida resuelve de otras entradas. Lo que dependa de la fecha (A-28, el reloj del servidor y su calendario de cambio de hora) NO se cierra con una sola ejecución: se anota la medida y espera a las ejecuciones 2 y 3.
> NO cambia: el motor ni la estrategia, salvo lo que mande la PARADA. Nadie ejecuta uv run botsito motor arnes salvo para medir según ADR-0070, y solo si lo autorizo en la PARADA. No se toca material del corpus ni del holdout.
>
> FASE 0, inventario sin tocar knowledge ni código, con PARADA antes de cambiar valores:
> a) Congela el CSV: su hash en un manifiesto nuevo en data/manifests/ (inmutable tras commit), con el procedimiento que pida el repo para data/demo_ftmo/ (DEMO-FTMO.md, «Dónde queda el fichero»). Léelo con uv run python scripts/leer_demo_ftmo.py data/demo_ftmo y pega la tabla en el informe.
> b) Tabla medida → decisión: para cada fila del CSV, a qué decisión o supuesto responde (ADR-0057 d1-d5 y §5, A-27, FTMO-REGLAS R9/R11/R12, el perfil knowledge/cuentas/ftmo-2step-swing-100k.yaml, parametros.yaml), qué dice hoy el repo y qué dice la medida. Marca si coincide, si contradice o si hoy es UNKNOWN y la medida lo fija. Como mínimo: stops_level y freeze_level (0), volumen_min/max/paso, modos de llenado (FOK e IOC), modo de ejecución, caducidades, swap, apalancamiento (30), comisión por lado (0,03 con 0,01 lotes), deslizamientos, y el llenado de la buy stop.
> c) modo_margen = ACCOUNT_MARGIN_MODE_RETAIL_HEDGING (la barra de título de MT5 también dice «Hedge»). Corrige la línea «Netting o hedging: SIN COMPROBAR» de DEMO-FTMO.md («La prueba de octubre de 2026») con lo medido. Mide qué supone hoy el simulador (¿una posición a la vez?, ¿qué pasa si se llena una orden con otra posición abierta?) y si netting o hedging lo cambiaría. Si la cuenta Swing real podría diferir de la prueba, apúntalo como pregunta a FTMO (por la vía de RESPUESTAS-FTMO, parafraseada), no como supuesto.
> d) La sell limit en el nivel exacto se llenó al instante (fila 41, «SE LLENO al instante»): compárala con la deuda «EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL» (su texto entero en HISTORIA, Archivo 1, dice «Sigue PENDIENTE medir en la demo lo que hace MT5»). Di si esta medida la paga, en parte o entera, o si no es el mismo caso.
> e) La fila 57 (buy_stop_llenado) trae retcode 0 «SIN_RESPUESTA» con «llenada»: lee el script (tools/mql5/MedirDemoFTMO.mq5) y explica si es lo esperado al leer un llenado (sin petición propia) o un defecto. No cambies el script en esta rama.
> f) A-28: anota desfase_servidor_gmt_min = 180 (servidor 15:35, GMT 12:35, local de Lima 07:35, horario de verano en Europa) como la primera de tres medidas, sin cerrar A-28.
> g) Pendiente heredado A4: decide con la medida si la propuesta de adelantar la negativa por A-27 (ADR-0057 §5, MEMORIA-SUITE.md:97-99) sigue teniendo objeto. Propón aplicarla, descartarla o dejarla para las ejecuciones 2 y 3, con su porqué.
> h) Next Action M (el break even de una venta que salta por el ASK, ADR-0065 §6): di si esta ejecución lo mide. Si no lo mide, se queda.
> i) Tu propuesta: qué valores cambian en knowledge/ (cada uno con su fuente; si el trailer Fuente: no admite un manifiesto, propón cómo citar: un ADR nuevo que cite el manifiesto, una evidencia documental…), qué ambigüedades se cierran (A-27, ¿con una ejecución?) y con qué forma (runbook AMBIGUEDADES.md), qué deudas se pagan, qué entradas de la Next Action cambian, y el texto de DEMO-FTMO.md que se corrige («unos cinco minutos» → lo medido).
> Entrega la fase 0 en el informe y PARA.
>
> FASE 1 (tras mi respuesta): lo que yo decida en la PARADA, cada cambio de valor con su trailer Fuente: y con ids que existan; tocar ambigüedades obliga a botsito spec docs --escribir en el mismo commit.
>
> Cierre de la rama:
> - make check > make-check.log 2>&1, con el exit 0, ningún failed y la línea SELLO, antes de cada commit.
> - Si la fase 1 toca código del simulador o de la plataforma, empuja la rama como fix/demo-ejecucion-1 y pasa la CI de Linux. El único fallo aceptado es el de state check por el nombre fix/. Dame los números de run.
> - Informe en docs/validation/DEMO-EJECUCION-1.md, con la fase 0, la PARADA y mi respuesta tal cual, y su estado al final.
> - Pasa el revisor (subagente revisor), con este alcance: que cada valor cambiado salga de una fila del CSV congelado; que no se cierre nada que dependa de la fecha; que la entrada A siga en pie para las ejecuciones 2 y 3. Pega su informe al final del tuyo.
>
> Rama lista para revisión, NO cerrada.
