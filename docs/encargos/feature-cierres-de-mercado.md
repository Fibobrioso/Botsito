# Encargo · feature/cierres-de-mercado

Dado por Aleks (consultor) el 2026-10-02. Copiado tal cual:

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Rama nueva: feature/cierres-de-mercado, desde main (5947e55, tag stable/F36p-freno-peticiones). Es A3 e) de «Pendientes heredados». Tarea autónoma: NO se cierra.
>
> Objetivo: que el bot no abra ni coloque operaciones en la ventana prohibida por FTMO antes de un cierre de mercado largo, según lo que FTMO dijo por escrito.
>
> Fase 0 · Inventario y diseño, antes de escribir código:
> - Copia literal de la regla: docs/validation/FTMO-REGLAS.md y la respuesta del ticket de soporte VDW-DPMWR-965 (donde esté en el repo). Qué prohíbe exactamente: abrir, colocar órdenes pendientes o mantener posiciones; cuántas horas antes; qué cuenta como cierre «largo» (2 h o más). Si algo de esto no consta por escrito, apúntalo como pregunta a soporte de FTMO; no lo supongas.
> - Qué cierres afectan a EURUSD en la ventana del trader (07–15 en España): fines de semana, festivos de los mercados que cierran el FX, cierres anticipados (Navidad, Año Nuevo…). Di de dónde sale cada uno.
> - La fuente del calendario: versionada en el repo (por ejemplo, un YAML de cierres conocidos por año) o leída del servidor. Dentro del bot, el horario de sesiones del símbolo en MT5 (SymbolInfoSessionTrade) es la fuente natural en vivo. Propón cómo se cruzan las dos y qué pasa si discrepan: gana la más restrictiva.
> - En qué reloj se calcula la ventana prohibida (el del servidor de FTMO; ADR-0063) y cómo se comporta con el cambio de hora.
> - Escribe el diseño en el informe antes de implementar.
>
> Fase 1 · Implementación:
> - Un predicado único «ventana_prohibida_por_cierre(instante)» que consultan las reglas que abren o colocan órdenes. Vive donde ninguna regla pueda saltárselo, como el freno.
> - Lo que hace dentro de la ventana: no abre ni coloca. Para órdenes pendientes ya puestas y posiciones abiertas, solo lo que diga la regla escrita de FTMO. Si la regla no lo dice, parámetro PROVISIONAL colgado de una ambigüedad abierta nueva, con la pregunta a soporte.
> - Las horas de margen, como parámetro del registro (ADR-0002), con la cita de la regla.
> - Todo bloqueo queda en el log con su motivo.
>
> Fase 2 · Tests, rompiendo la guardia a propósito:
> - un viernes: no se abre dentro de la ventana previa al cierre del fin de semana y sí justo antes de que empiece;
> - un festivo con cierre anticipado sintético;
> - el cambio de hora (último domingo de octubre) no mueve la ventana de forma incorrecta;
> - un día normal no bloquea nada;
> - con el predicado desactivado, los tests fallan.
> Sin cobertura agregada sobre las 77.
>
> Informe en docs/validation/CIERRES-DE-MERCADO.md, con las preguntas para soporte de FTMO redactadas en inglés, si quedan. Si tocas algo dependiente de la plataforma, CI de Linux por fix/. make check sellado, revisor con su informe pegado. PROJECT_STATE por debajo de 23.000 bytes.
> «Rama lista para revisión, NO cerrada.»
