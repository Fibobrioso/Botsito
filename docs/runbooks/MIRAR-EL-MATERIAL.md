# Mirar el material: fotogramas, transcripciones y el reloj de FX Replay

Lo que hace falta SOLO cuando una tarea abre fotogramas, lee transcripciones o compara el video con
las velas. Mudado TAL CUAL desde `CLAUDE.md` («Que se puede mirar y que no» y «Donde esta el texto
de las transcripciones») el 2026-10-01, en `trabajo/dieta-y-skills`; alli queda la regla corta
y el puntero a este fichero. Las fechas y los «hoy» son los de cuando se escribio cada parrafo.
Lo que se puede mirar y lo que no lo sigue diciendo `CLAUDE.md`: esto es el COMO.

Estan infrautilizados, y eso cuesta turnos del trader: hay **25.372 PNG a 1 fps** de los seis videos y
solo **8 fotogramas distintos, citados por 9 items de 365** el 2026-09-17 (dos de esos ocho los
cito aquella misma rama). Medido de nuevo el 2026-09-25 con el mismo recuento (ids
`fr-…/<ms>` dentro de `knowledge/evidence/`): **13 fotogramas distintos, citados por 12 items de
368**. Sigue siendo muy poco. La auditoria del 2026-09-13, epigrafe *Fotogramas no abiertos*, ya lo decia: los "aqui"
de v4 1:06:12, v1 0:14:54 y el bloque de origen siguen sin abrirse, y entonces `data/fotogramas` ni
siquiera estaba copiado. **Una pregunta de geometria se contesta muchas veces mirando el fotograma, sin
gastarle un turno al trader** (asi se resolvio el breaker de M1: `docs/validation/BREAKER-M1.md`).

> **Por que cambio esta regla, TERCERA vez (2026-09-21).** Hasta hoy el segundo punto prohibia
> "el detalle por operacion de los xlsx del corpus" EN BLOQUE, sin distinguir dias. Los dos
> documentos que mandan ya eran granulares por dia -`ADR-0021` §1 dice "en esos dias" desde el
> 2026-09-12, y `ADR-0025` §4 autoriza los 6 `dev` de mayo-, asi que este fichero volvia a ser MAS
> ESTRICTO QUE EL ADR sin que ningun ADR lo dijera, y tomado al pie de la letra prohibia F14a
> entera: la ingesta del detalle de los dias `dev`, que es el paso que el proceso exige. Corregido
> con ADR-0037, que ademas anade lo que faltaba y no estaba en ninguna parte: la regla para un
> fichero que MEZCLA granularidades, y la regla para leer estructura sin leer valores.
>
> **Por que cambio esta regla (2026-09-20).** Hasta hoy decia que el backtest de septiembre no se
> abria "hasta que sus particiones esten sorteadas y commiteadas". Estaba MAL ESCRITA desde el
> principio: bloqueaba un paso que el propio proceso exige, porque sin saber que dias cubre el
> material no hay universo que sortear. **Es la segunda vez que pasa lo mismo, y eso ya es un
> patron, no una anecdota**: la obligacion 6 de `HOLDOUT-EXPOSICIONES.md` prohibia ejecutar
> `kit check` y `kit build` con `data/` presente y dejaba la sesion 2 bloqueada para siempre
> (reescrita el 2026-09-17, ADR-0033). **En los dos casos este fichero era MAS ESTRICTO QUE
> ADR-0021 sin que ningun ADR lo dijera.** De ahi la regla de la regla: una prohibicion escrita
> aqui que no salga de un ADR se revisa antes de aplicarla, porque puede estar prohibiendo un paso
> necesario; y si se aparta de ADR-0021, o se corrige aqui o se cambia el ADR, pero no se deja el
> desacuerdo por escrito.

**COMO SE ABRE UN FOTOGRAMA: POR INSTANTE LOCALIZADO, NUNCA POR MUESTREO** (ADR-0038). Un
fotograma se abre solo en un instante que se haya localizado ANTES -por la transcripcion, por un
item de evidencia que ya lo cite, o por una marca de tiempo ya registrada-, y el vecindario
inmediato de un instante ya citado cuenta como localizado. **LA VIA DE LOCALIZACION ES LA
TRANSCRIPCION**, que ademas es mucho mas barata que barrer imagenes.

Es PROCEDIMIENTO y no una prohibicion nueva de contenido: lo que se puede mirar no cambia. El
motivo es que **no se puede saber que hay en un PNG antes de abrirlo**, asi que muestrear a
ciegas es incompatible con que una clase entera de imagenes -las capturas de Analytics- este
prohibida. Si un fotograma abierto asi resulta traer un AGREGADO, se declara el MISMO DIA con sus
cifras listadas y ninguna se usa (ADR-0021 §2, ADR-0038 §2). Medido el 2026-09-22: muestreando v4
se abrio la pestana Analytics de agosto; el mismo muestreo sobre v1 o v2 habria caido sobre mayo
o julio, que SI tienen dias reservados.

**EL RELOJ DE LOS GRAFICOS DE FX REPLAY ES UTC+2 FIJO.** Medido en el propio grafico de v4 sobre
un fotograma de ENERO -asi que NO es Europe/Madrid, que en enero es UTC+1-; confirmado porque con
ese desfase las velas de abril casan a 1 y 2 puntos con las de Dukascopy. Es una propiedad del
INSTRUMENTO y la necesita toda comparacion futura entre video y velas.

**Y LA REGLA QUE SALE DE AHI: antes de comparar dos fuentes se FIJA EL HUSO DE LAS DOS, medido y no
supuesto**, igual que las cabeceras se escriben antes de abrir el libro. El pre-registro impide
elegir el criterio despues de ver los datos; NO impide equivocarse al instrumentar, y la rama
`trabajo/abril-y-la-caja` lo demuestra: con los criterios congelados y respetados, suponer que el
eje del grafico era UTC dio una conclusion falsa -"las series no cuadran"- que estuvo a punto de
cerrar la rama. Lo que lo destapo fue mirar un fotograma de OTRO video por un motivo distinto.

## Donde esta el texto de las transcripciones

Es lo que mas tiempo hace perder. `knowledge/corpus/transcripciones/` solo tiene los MANIFIESTOS YAML
(`tr-<video>-<modelo>-<hash>.yaml`), no el texto.

- **El texto bueno:** `data/transcripciones/<video>/<modelo>/` -por ejemplo
  `data/transcripciones/v1/large-v3-int8-float16/`- con `cruda.jsonl`, `cruda.txt`, `corregida.jsonl`,
  `correcciones.jsonl`, `fragmentos/` y `parciales/`. La CRUDA es de la que se copia una cita literal.
- **Version legible para buscar:** `corpus/Estrategia del trader/_procesado/transcripciones/*.txt`
  (7 ficheros). Es el ASR pequeno heredado, con deriva de hasta un minuto (ADR-0007): sirve para
  LOCALIZAR, no para citar literal.
- **Los segmentos CRUDOS estan copiados dentro de `knowledge/_proposals/*.yaml`**, en
  `contexto.segmentos` (con `n`, `t0_ms`, `t1_ms`, `texto`, `senales`): suele ser la via mas rapida
  para ver el tramo que rodea a una evidencia.
