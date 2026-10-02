# Encargo · feature/freno-peticiones

Dado por Aleks (consultor) el 2026-10-02. Copiado tal cual:

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Rama nueva: feature/freno-peticiones, desde main (695041d, tag stable/F36o-cerrar-a29-a36). Es la K de Next Action. Tarea autónoma: NO se cierra.
>
> Objetivo: que el bot no pueda superar el límite de mensajes al servidor de FTMO (2.000 al día, docs/validation/FTMO-REGLAS.md), pase lo que pase en el código que lo llama.
>
> Fase 0 · Inventario, antes de escribir código:
> - Las siete reglas que envían peticiones (medido en feature/escenarios-por-sesion): cuáles son, qué cuenta hoy el contador, y en qué reloj se reinicia el día (el de FTMO, no el de la sesión; ADR-0063).
> - Qué cuenta FTMO como mensaje: verifícalo en FTMO-REGLAS.md y en lo que diga la demo (ADR-0057). Si no consta, apúntalo como pendiente de la demo, no lo supongas.
> - El diseño, escrito en el informe antes de implementar.
>
> Fase 1 · El freno, con estos principios:
> - Vive en el adaptador del bróker (el puerto), no en las reglas de la estrategia: ninguna regla puede saltárselo.
> - Dos umbrales, como parámetros del registro (ADR-0002): uno de aviso y uno de corte, por debajo de 2.000 con margen. Valores PROVISIONALES colgados de una ambigüedad abierta nueva (la regla del test de PROVISIONAL), con su motivo.
> - Al llegar al corte: no envía nada más ese día salvo lo que proteja la cuenta (cerrar o cancelar). Decide y justifica si cancelar o cerrar cuenta para el límite, y que nunca quede una posición sin stop por culpa del freno.
> - Además del total diario, un freno contra bucles: N peticiones iguales seguidas en poco tiempo detienen el envío y lo registran. También parámetro PROVISIONAL.
> - Todo corte queda en el log con su motivo.
>
> Fase 2 · Tests, rompiendo la guardia a propósito:
> - un bucle sintético que intenta 5.000 peticiones no pasa del umbral de corte;
> - al llegar al corte, una orden de cierre o cancelación sí sale;
> - el contador se reinicia con el día de FTMO, no con la sesión;
> - ninguna posición queda sin stop por el freno;
> - el día normal medido (10 a 13 peticiones) no toca ningún umbral.
> Sin cobertura agregada sobre las 77.
>
> Informe en docs/validation/FRENO-PETICIONES.md. Si tocas algo dependiente de la plataforma, CI de Linux por fix/. make check sellado, revisor con su informe pegado. PROJECT_STATE por debajo de 23.000 bytes; la K pasa a HISTORIA solo al cerrar.
> «Rama lista para revisión, NO cerrada.»
