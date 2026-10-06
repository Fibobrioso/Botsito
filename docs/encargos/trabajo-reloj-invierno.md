# Encargo · trabajo/reloj-invierno

Dado por Aleks (consultor) el 2026-10-06. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva trabajo/reloj-invierno, desde main en 25469ff (tag stable/F37b-guardias-citas; verifica con git que main y origin/main están ahí antes de abrir). Ábrela con la skill abrir-rama: este prompt tal cual en docs/encargos/trabajo-reloj-invierno.md, su contrato.yaml y el archivo de PROJECT_STATE en HISTORIA.
>
> Objetivo: medir con material de construcción de invierno (enero de 2026) qué reloj tiene el gráfico del trader y en qué horas UTC opera en invierno, antes de activar A-42 (Next Action E). Es una rama de MEDIDA.
>
> Qué NO cambia: motor, strategy_spec, parametros.yaml (reloj_sesiones, huso_grafico, anclaje_h4), ambiguedades.yaml (A-42 sigue ABIERTA), knowledge/evidence y corpus. Febrero y marzo no se tocan ni se listan. Nada del backtest de julio (punto S). Ningún fotograma por muestreo.
>
> Contexto que entra al encargo (hasta hoy fuera del repo):
> 1. Respuesta del trader al punto E por WhatsApp, 2026-10-06, hora de Lima, literal: 09:53 «según la configuración de la plataforma etc+2 madrid»; 09:59 «xd» «sep» «seria cuestion que se adapte a lo que bote la plataforma». No dio las horas de cierre de las velas de 4 horas.
> 2. Captura del selector de zona horaria de su plataforma, que NO entra al repo: tiene marcada «(UTC+2) Madrid»; en la misma lista Londres, Lisboa y Dublín salen como (UTC+1); el reloj del pie marcaba 18:22:55 UTC+2. Es una captura de configuración, no de Analytics ni de operaciones.
> Registra el punto 1 como exija el repo para una respuesta escrita del trader (feedback, medio escrito, literal), en commit propio con Fuente:. Si el procedimiento pide algo que aquí no está, para y dímelo.
>
> Hipótesis del consultor, escritas ANTES de medir (cópialas al informe sin tocarlas):
> - H1 (lectura de ADR-0059): gráfico en UTC+2 fijo y sesiones fijas 07–15 en ese reloj; en enero opera 05:00–13:00 UTC.
> - H2: gráfico en Europe/Madrid con cambio de hora (el selector muestra el desfase de hoy); en enero opera 06:00–14:00 UTC. Dos variantes que enero no separa: H2a, 07–15 de reloj civil de Madrid; H2b, las sesiones son las velas H4 de la rejilla de anclaje_h4 que en verano caen 07–11 y 11–15 (01:00–09:00 de Nueva York). Solo se separan cuando Europa y EE. UU. no coinciden en el cambio de hora.
> - Hoy el UTC+2 fijo sale del fotograma fr-v4-9ad0ebb8/1200000 («14:29:59 UTC+2» sobre «Thu 29 Jan '26», ABRIL-Y-LA-CAJA.md R0). v4 se grabó el 2026-08-30 (MESES-VISTOS.md), en verano: si el reloj del pie da la hora real de la grabación, marcaría +2 también con H2.
>
> Fase 0, inventario sin tocar nada:
> a. casos_reservados(repo) sobre enero de 2026: ningún día en ninguna partición. Si hay alguno, PARA.
> b. Dónde está el xlsx de enero, su sha, que no está en libros.yaml, y que el dataset eurusd-m1-2026-01-e37291d4 está completo.
> c. Qué fotogramas de v4 hay alrededor de 1200000 (sin abrirlos) y qué instantes de v4 localiza la transcripción en los que el trader lee una vela de enero con su leyenda O/H/L/C.
> d. Declaración en HOLDOUT-EXPOSICIONES.md de lo que se va a leer, el mismo día.
> Entrega la fase 0 en el informe y sigue sin esperarme solo si a. sale limpio y nada pide decisión.
>
> Fase 1, en este orden:
> M1. Huso del libro de enero con el procedimiento de libros.yaml tal cual (entrada dentro de la M1 ±2 puntos, UTC frente a Europe/Madrid, control sobre agosto y abril, ≥90 % / ≤50 %). Añade Etc/GMT-2 como tercer candidato SOLO como dato, sin cambiar el umbral. Si sale concluyente, declara el libro (solo añadir). Si no, NO CONCLUYENTE y M2 no se ejecuta.
> M2. La decisiva. Con las horas de entrada de enero en el huso de M1, cuenta las entradas en [05:00, 06:00) UTC y en [13:00, 14:00) UTC, y lista sin interpretar las que caigan fuera de [05:00, 14:00) UTC. Regla escrita ahora:
>    - H2 si hay ≥3 en [13:00, 14:00) y 0 en [05:00, 06:00);
>    - H1 si hay ≥3 en [05:00, 06:00) y 0 en [13:00, 14:00);
>    - cualquier otra cosa, NO CONCLUYENTE.
>    Control: el mismo recuento sobre agosto y abril (verano: H1 y H2 predicen las dos [05:00, 13:00) UTC). Si el control tiene entradas en [13:00, 14:00), dilo antes del veredicto de enero, porque la regla dejaría de discriminar.
>    Solo horas y recuentos: ni resultados, ni R, ni PnL.
> M3. El reloj del pie de v4. Abre fr-v4-9ad0ebb8 en 1200000 con --n (instante ya localizado). Mide si el reloj avanza al ritmo del vídeo aunque las velas no se muevan (hora real) o si va con el replay. Si la fase 0 c dio una vela de enero con leyenda y hora del eje, compárala con Dukascopy suponiendo eje UTC+1 y eje UTC+2, como en ABRIL-Y-LA-CAJA R0, con la diferencia máxima en puntos de cada una.
> M4. Tabla calculada con zoneinfo, no a mano, de la rejilla H4 de anclaje_h4 (17:00 America/New_York) para 2025-10-20/24, 2025-10-27/31, 2025-11-03/07 y una semana de enero de 2026: hora de apertura de las velas de la mañana en UTC, Europe/Madrid y Etc/GMT-2. Al lado, qué predice cada hipótesis (H1, H2a, H2b) para la respuesta del trader en S-7 (SESION-04-EXTRACCION.md §3.1).
>
> Informe en docs/validation/RELOJ-INVIERNO.md: las hipótesis tal cual, cada medida con su salida, el veredicto por la regla escrita y lo que NO decide. Si la medida contradice «UTC+2 FIJO», añade una línea de Technical Debt que apunte al informe, sin borrar la vieja, con saldo de bytes de PROJECT_STATE ≤ 0. No corrijas ABRIL-Y-LA-CAJA, MIRAR-EL-MATERIAL ni huso_grafico: eso va en la activación de A-42.
>
> Para la activación (escríbelo en el informe, sin implementarlo): el bot corre en el MT5 de FTMO, no en la plataforma del trader, así que su ventana se fija en instantes UTC calculados con zoneinfo; el reloj del servidor de FTMO (A-28) solo traduce sus marcas de tiempo y se mide en la demo.
>
> make check y uv run botsito state check en verde. Si acabas tocando hooks o rutas, push de fix/reloj-invierno y CI de Linux con su número de run. Revisor con su informe pegado al final; que compruebe aparte que la regla de M2 está en el encargo antes que la salida de M2 y que no se leyó nada de febrero, marzo ni julio.
>
> Rama lista para revisión, NO cerrada.
