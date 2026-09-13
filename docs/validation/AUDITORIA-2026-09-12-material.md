# Auditoría del material recogido — 2026-09-12

**Qué se auditó:** todo el material que el trader ha entregado y todo lo que el proyecto ha
derivado de él, buscando dos cosas: material sin usar, y preguntas que damos por abiertas y el
corpus ya responde.

**Por qué se hizo:** el consultor descubrió que había **tres exportaciones de backtest** (enero,
abril, agosto) que llevaban nueve días en el corpus sin que nadie las usara, mientras se planificaba
F14 sobre seis días. Preguntó si habría más cosas así. Las hay.

**Cómo:** tres barridos en paralelo —inventario, conocimiento y material visual— con la misma
restricción dura: **ningún detalle de los 13 días reservados de mayo**. Todo lo que sigue está
verificado ejecutando; lo que es hipótesis se marca.

---

## 0. Lo que hay que hacer con esto, en orden

| | Qué | Necesita al trader |
|---|---|---|
| 1 | **`liquidez_tomada` no se apaga nunca** (§2.1). El motor reentraría sobre la misma liquidez indefinidamente | no |
| 2 | ~~¿Se cierra el trade al vencer la H4 de las 11:00?~~ **RESPONDIDA el 2026-09-12** (§2.2): corre hasta las 15:00. Gana RN-002 y la spec no cambia | hecho |
| 3 | **No existe regla que diga QUÉ nivel es la liquidez de M15** (§2.3). Sin ella F18 no se puede construir fiel | no |
| 4 | **El token `equal` está mal definido y RN-019 nunca dispararía** (§2.4) | no |
| 5 | **Cinco items vivos contradicen reglas ya corregidas** (§2.5) | no |
| 6 | **A-18 está respondida cuatro veces, con aritmética** (§3.1) | no |
| 7 | **La contradicción `stop.nivel` tiene su literal en v6, dos veces** (§3.2) | no |
| 8 | **La observación de invierno que ADR-0015 daba por inexistente, existe** (§3.3) | no |
| 9 | Pedirle **junio** —el mes que ya debe— y la captura de la pestaña `Prop firm` (§5) | **sí** |

### Lo que se aplicó en esta misma rama

| | Qué se hizo | Dónde |
|---|---|---|
| 1 | **`stop.nivel` CERRADA**, la única contradicción abierta del proyecto. Dos citas de v6 superseden a los items que sostenían 0,75 — y a **dos más** que nadie había visto, en temas hermanos | 11 items nuevos en `knowledge/evidence/v6/` |
| 2 | **A-18 gana su cita**: la aritmética de v6 solo cuadra con la caja completa | `ev-v6-014702-2d7096db` |
| 3 | **El ganador no apaga el día**: tres items superseden a los tres que decían lo contrario | `ev-v6-000732-*` |
| 4 | **RN-010 fija `operacion_abierta`** (§2.6): una entrada activada por un `equal` era invisible para el cierre forzoso y para el break even | `strategy_spec.yaml`, spec 10.2.0 |
| 5 | **La guardia de contradicciones dejó de morderse la cola**: exigía que siguiera ABIERTA, así que cerrarla invalidaba el registro que la cierra | `contradicciones.py`, `feedback/modelo.py`, `cli.py` |
| 6 | **El golden de F07 mide la extracción, no la vigencia**: un item supersedido sigue siendo un registro fiel de lo que se dijo | `test_golden_citas_f07.py` |
| 7 | **`vistos.yaml` deja de decir un dato falso** sobre la columna de fecha de agosto | `vistos.yaml` |

**Lo que NO se aplicó, y por qué:** el ciclo de vida completo de los hechos (§2.1, §2.3, §2.4)
está diseñado y **bloqueado por un defecto del propio diseño**, en
`docs/plan/features/F14b-ciclo-de-vida-de-los-hechos.md`. Resumido: apagar `liquidez_tomada`
mientras dure `detenido_por_cartuchos` —que no se apaga nunca— dejaría el bot muerto tras agotar
cartuchos la primera vez. Antes de escribir esas reglas hay que decidir **si un hecho se apaga con
una regla o se declara con su duración dentro**, porque hoy conviven las dos formas y ninguna está
documentada como la buena.

### §2.6 · RN-010 no declaraba que hubiera posición viva

Encontrado al revisar el token `equal`. RN-010 gestiona la entrada activada por un `equal`
(`gestionar_salida`) pero **no fijaba `operacion_abierta`**, el hecho que consumen RN-002 (cierre
forzoso a `ventana_fin`) y RN-014 (break even). Una entrada por `equal` no se habría cerrado a las
15:00 ni habría llegado nunca a break even. Es el mismo defecto que la auditoría de F12 encontró
con `liquidez_tomada`, en otra regla. Corregido, y el test pasa a exigir **dos** productores en vez
de fijar uno.

---

## 1. El material, y cuánto no se usaba

**Inventario sano**: 513 ficheros + 6 vídeos declarados, 519 en disco, sha256 y bytes cuadran.
Cero ausentes, cero sobrantes, cero hashes rotos.

**Lo que no se usaba**, por lo que vale:

| Material | Estado |
|---|---|
| **3 xlsx (enero 58 ops, abril 38, agosto 47)** | 0 items de evidencia, 0 feedback, 0 lectores en `src/`. 143 operaciones con hora, dirección, entrada, SL y R |
| **v6, la sesión 1 (147 min)** | **3 %** cubierto por evidencia. Con los 28 feedback que llevan minuto, quedan **66 minutos en huecos**, y no son silencio: 5–9 min de habla por cada 10 |
| **21 capturas de Analytics** | ninguna citada. El proyecto las llama *"15 capturas de balance"* (F03) y son la pestaña Analytics **entera** de enero y agosto |
| **v2 38:30–56:00** (21 min) | nunca entró en ninguna propuesta. En 40–43 min habla de noticias |
| **2 PNG de WhatsApp de la entrega de mayo** | ningún registro los cita |

**La Cuarta parte de la hoja de la sesión 1 está en blanco**: el etiquetado ciego de los 16 días no
se hizo, ni en papel ni en vídeo. Eso explica los cero `LABEL_CASE` y confirma que la verdad de
F14 sale de los xlsx.

---

## 2. Defectos de negocio en la spec

### 2.1 · `liquidez_tomada` se enciende y no se apaga nunca

`liquidez_tomada` aparece tres veces en `strategy_spec.yaml`: `se_da_esquema` la exige (`depende_de`),
RN-004 la pone en `"si"`, y **nadie la pone en `"no"`**. Una vez tomada la liquidez de M15, el
hecho queda encendido indefinidamente, también de un día para otro.

Es la misma familia del defecto que la auditoría de F12 encontró el 2026-09-11 —entonces el hecho
ni estaba declarado y el bot habría entrado *sin esperar* la toma—. Ahora está declarado, se
enciende, y no se apaga.

El corpus dice cuándo hace falta una liquidez **nueva**, con tres condiciones que ninguna regla recoge:

- **tras una ganadora** — v6 0:32:27–0:32:55, *"ya aquí está el trade ganador, aquí no buscamos
  nada […] tenemos que esperar nuevamente a que se desarrolle la liquidez"* (**sin item**);
- **tras agotar cartuchos** — `ev-v3-005617`, `ev-v4-002401`, `ev-v4-005151`;
- **tras una pérdida con cartuchos vivos**, se reintenta sobre la MISMA liquidez pero exigiendo
  estructura nueva y *fuera* — `ev-v4-003820`: *"no puedes volver a entrar hasta que se cierre esta
  zona de control y te genere otra […] tiene que ser nuevamente afuera"*.

### 2.2 · Su ficha cierra el trade a las 11:00; la spec, a las 15:00

`ev-v3-010304-4468cc20` (confirmado, de su ficha de reglas): *"cierra la vela de H4 operativa, se
cierra el trade porque ya la siguiente vela es otro movimiento"*, `valor: si`.

RN-002 solo cierra en `ventana_fin`. Un trade abierto a las 10:58: según su ficha se cierra a las
**11:00**; según la spec corre hasta las **15:00**. El detector no lo ve porque están en temas
distintos, y A-6 no cita ese item.

**RESUELTA el 2026-09-12.** El trader, por el consultor: *"se deja correr hasta las 3pm, a esa
hora se cierra la operativa total"*. Gana **RN-002** y la spec **no cambia**; lo que queda viejo es
`ev-v3-010304`, corregido por `fb-2026-09-09-sesion-01-2e300aab`. Ese registro es además **el
primero que usa `recibido_el` para lo que ADR-0023 lo creó**: la sesión es del 9 y la respuesta
llegó el 12.

### 2.3 · No hay regla que diga qué nivel *es* la liquidez de M15

El token `liquidez_m15` se usa como si estuviera dado. El corpus lo define y nadie lo ha escrito:
el pivote de M15 marcado por una vela contraria al flujo (`ev-v4-003451`, `ev-v4-005749`; v6
0:37:01 *"vemos una vela contraria, este par de velas nos indica que ya se puede marcar la
liquidez"*, **sin item**), el más reciente (`ev-v1-001334`; `ev-v4-010921` *"de hace 2 o 3 días no
se toma"*), ya formado (`ev-v4-005053`), en el lado contrario al sesgo (v6 0:03:21, 0:18:51) y *"la
zona más baja que me deja el precio"* (`ev-v3-001531`).

Sin esta regla, F18 no puede construirse fiel.

### 2.4 · El token `equal` está mal definido, y RN-019 nunca dispararía

`strategy_spec.yaml` lo define como *"la operación cerró sin ganancia ni pérdida"*, y contradice al
glosario (*"dos extremos al mismo precio"*). En el corpus un `equal` es **geometría que activa la
límite sin ruptura**, y ese trade puede acabar en pérdida: `ev-v5-000246` *"contarlo como pérdida,
pero reentrar"*; v6 1:23:13 *"te genere un equal, te saque la entrada, te genera una pérdida, pero
luego caiga […] abrimos otra orden límite para poder reentrar"*.

RN-019 (`se_cierra_operacion: {resultado: equal}`) no se dispararía nunca tal como está.

### 2.5 · Cinco items vivos contradicen reglas ya corregidas

Ninguno tiene `supersede`, así que siguen alimentando la evidencia y el detector:

| Item | Dice | Contra |
|---|---|---|
| `ev-v1-000959`, `ev-v3-002714`, `ev-v4-011351` | el ganador apaga el día | RN-017 (v6 0:07:32: *"no estamos pausando cuando se dé el trade ganador"*, **sin item**) |
| `ev-v3-005046` | una entrada invalidada consume cartucho | `cartucho_criterio` (`fb-…-aa2abe65`) |
| `ev-v3-011200` | el barrido basta con la mecha | `liquidez_m15_criterio_toma = cuerpo`. **Hipótesis**: v3 habla del *barrido* y v4/v6 de la *toma válida*; si es así, el glosario debe distinguirlos |

---

## 3. Lo que ya estaba respondido

### 3.1 · A-18 (base del 1:3): cuatro veces, con aritmética

`ev-v1-000948` *"3 menos 0.75 sería 2 con 25"* · `ev-v4-011742` · `ev-v4-011856` *"12 x 3 son 36 …
0.75 por 9 sería 6.75"* · y **v6 1:46:43–1:47:52, sin item**: *"usando 075 en 3 nos mantendríamos
en un beneficio de 2,25 […] como manejamos a 0,80, 3 perdedores y el cuarto ganador, tenemos un
margen de 0.60"* (3 − 3×0,8 = 0,6).

Solo cuadra con `base_calculo_objetivo = caja_completa` —el valor que ya corre— y con el RR
realizado 3/0,8 = 3,75 que RN-015 declara. **Se cierra sin el trader.**

### 3.2 · La contradicción `stop.nivel` tiene su literal

v6 1:35:08 *"era 0 75 … bueno 0 80. Hay que hablar con 0.80 porque manejamos 0.80"* y v6 2:19:39
*"Es 0.80 … Ahora es a 0.8, no a 0.75"*. Dos items nuevos con `supersede` sobre `ev-v1-000448` y
`ev-v2-003142`, regenerar, y cierra. **Sin el trader.**

### 3.3 · La observación de invierno que ADR-0015 daba por inexistente

ADR-0015: *"**todas las lecturas del repositorio son de verano** […] `Etc/GMT-2` y `Europe/Madrid`
son indistinguibles de mayo a octubre"*. Sobre esa falta se degradó `huso_grafico` y se abrió A-14.

Medido sobre las horas `dateStart` de sus propios xlsx —no sobre el eje de un gráfico—:

| Mes | Horas UTC | Desfase | Hora local |
|---|---|---|---|
| **Enero** (CET, UTC+1) | **06–13** | +1 | 07:00–14:xx |
| Abril (CEST, UTC+2) | 05–12 | +2 | 07:00–14:xx |
| Agosto (CEST, UTC+2) | 05–12 | +2 | 07:00–14:xx |

Su hora de pared es idéntica en las dos mitades del año y sus horas UTC se mueven con el cambio de
hora: **reloj civil con DST**, y un offset fijo queda descartado. Confirma empíricamente
`huso_operativa = Europe/Madrid` (ADR-0017) y la ventana 07:00–15:00. Cuatro meses, dos regímenes
horarios, cero contraejemplos.

### 3.4 · Nueve pérdidas consecutivas en enero, seis el mismo día

La captura de *Winners and Losers* de enero marca `Max consecutive losses: 9` (abril 6, agosto 3).
La evidencia del proyecto dice **7** (`ev-v4-000451`), tomada de v4 **a mitad del backtest** —los
fotogramas muestran 53 operaciones y PF 2,07 frente a las 58 y PF 3,01 del mes cerrado—. Ese item
no lo cita ninguna regla.

Reconstruido desde el xlsx: **el 2026-01-02 encadenó seis pérdidas en el mismo día**. Con el lotaje
de ADR-0020 —cada pérdida cuesta el 0,5 % entero— son **3,0 % de la cuenta en una sesión**, dos
tercios del tope diario del 4,5 %, el primer día de un mes que él presenta como bueno. RN-020 anota
que los cartuchos no acotan el día porque el contador se reinicia con cada liquidez de M15: **aquí
está el número que faltaba para dimensionar ese riesgo**.

*Detalle para F26*: FX Replay **no rompe la racha con un break even**. Contando ceros como no
interruptores salen 9/6/3, que es lo que muestran las capturas; contándolos como interruptores,
6/6/3. Si F26 compara rachas, tiene que usar esa convención.

---

## 4. Herramientas que no vigilan lo que creemos

1. **El detector de contradicciones compara solo dentro de un tema idéntico**, y la taxonomía
   asigna un tema nuevo casi por item. Lleva **0 detectadas de al menos 6 reales** (§2.2, §2.5, y
   los cartuchos 2-vs-3, que se resolvieron sin que el detector los viera).
2. **`vistos.yaml:12` dice un dato falso**: *"el xlsx de agosto no tiene columna de fecha"*. Sí la
   tiene —`dateStart`, rellena en 47 de 47, del 3 al 31 de agosto—. Con ella se sabría qué días vio;
   se excluyó el mes entero por un motivo que no era cierto.
3. **`manifest.yaml` no tiene campo de descripción para el material visual**. Por eso quince
   capturas de Analytics pasaron tres semanas etiquetadas como *"capturas de balance"*.
4. **`corpus/` está en `.gitignore`**, y `Material adicional`, `Sesiones` y v6 (9,8 GB) solo
   existen en esta máquina. En Drive no falta nada de lo que hay en Drive; esas tres cosas nunca
   subieron. Punto de fallo único sobre material irrepetible.
5. `data/drive_staging/` (655 MB) es un duplicado de lo ya subido a Drive.

---

## 5. Lo que hay que pedirle al trader, y cabe en un mensaje

1. **Junio de 2026**, el segundo mes que ya había acordado. Es el único material que cumple las
   tres condiciones a la vez: **no lo ha visto** (no está en `vistos.yaml`), **no aparece en ningún
   vídeo** (0 de 353 items lo mencionan) y **su partición ya está sellada** en el paquete de la
   sesión 1 —21 días, 10 `dev` / 2 / 4 / 5, con el seed commiteado antes de que exista ninguna
   etiqueta—. Además tiene OHLC congelado, así que no hace falta descargar nada. Aportaría **11
   días de holdout** sobre los 12 que quedan vivos.
2. **La pregunta del cierre a las 11:00** (§2.2).
3. ~~**Una captura de la pestaña `Prop firm` de FX Replay.**~~ **DESCARTADA el 2026-09-12**: el trader no la tiene configurada con FundedNext, así que no hay atajo y A-17 y A-19 siguen necesitando el reglamento y el panel de la cuenta. Anotado en las dos ambigüedades para que nadie lo vuelva a proponer. El texto original era: Tiene el plan Pro y esa pestaña
   contratada, y no la ha enseñado nunca. Si su simulador está configurado con FundedNext, el panel
   llevaría dentro **la ventana de noticias (A-17)** y **el corte del día de riesgo (A-19)**: las
   dos preguntas que hoy solo se pueden cerrar leyendo un documento externo. Cuesta un mensaje.

---

## 6. Lo que sigue genuinamente abierto

| Pregunta | Cómo se cierra |
|---|---|
| **A-16** (Oanda vs Dukascopy) | **Midiendo, y ya se puede**: sus xlsx traen el precio de entrada sobre velas de Oanda; comparar con la vela M1 de Dukascopy del mismo minuto da el margen. Solo sobre días `dev` |
| **A-17** (reglamento de noticias) | Documento externo, o la captura de §5.3 |
| **A-19** (reloj del día de riesgo) | Panel de FundedNext, o la captura de §5.3 |
| **A-13** (BE al toque o con cuerpo) | **Midiendo**: el corpus inclina 5 a 1 al toque, y él mismo pidió cuantificarlo. Ojo: `break_even_criterio_ruptura` y `zona_control_criterio_completada` son dos parámetros para el mismo predicado — la doble puerta que ADR-0002 prohíbe |
| **A-21** (zona limpia) | El corpus la operacionaliza: *limpia* = exactamente una zona de control, y el número de velas es indiferente (`ev-v3-004942`, `ev-v4-010425`, y v6 0:35:07 **sin item**). Lo que queda no es una pregunta, es que el mapeador cuente zonas como él — y eso se mide |
| **Nuevas** | H4 previa que rompe los dos extremos (y el sesgo del primer día); llenado parcial de la orden límite |
