"""Hoja de respuestas de una sesion con el trader, en Word (.docx). F10, ADR-0011.

Lee el paquete del kit (`knowledge/cases/kit/<sesion>/`) y el contexto humano de cada pregunta
(`knowledge/cases/kit/contexto_preguntas.yaml`) y escribe un documento pensado para rellenar a
mano durante la sesion: cada pregunta con su porque, sus citas exactas, como responder y una caja
de respuesta; y al final la tabla de etiquetado de los casos `dev`.

No inventa nada: las citas, los minutos, los fotogramas y los dias salen del cuestionario que
genera `botsito kit build`. Sin dependencias externas: un .docx es un zip de XML y aqui se escribe
a mano.

Uso:
    uv run --no-sync python scripts/hoja_sesion_docx.py
    uv run --no-sync python scripts/hoja_sesion_docx.py --sesion 2026-09-09-sesion-01
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from botsito.cases.paquete import (  # noqa: E402
    DIRECTORIO_KIT,
    cargar_config,
    esquema_paquete,
    sesiones_del_kit,
)
from botsito.comun.yaml_estricto import cargar_yaml  # noqa: E402
from botsito.config.registro import cargar_registro  # noqa: E402
from botsito.evidence.modelo import cargar_evidencia  # noqa: E402
from botsito.feedback.modelo import TIPOS_OBJETIVO  # noqa: E402

ANCHO = 9638  # A4 menos margenes de 2 cm, en twips
# La ambiguedad del anclaje de las velas H4: de ella salen la rejilla de horas que ensena la
# hoja y la captura de pantalla que hay que pedirle al trader.
ANCLAJE_H4 = "A-9"
# Tope de una cita en la hoja. La mas larga de hoy son 313 caracteres: el margen existe para
# que una cita literal que el trader tiene que confirmar no salga recortada.
LIMITE_CITA = 700
GRIS = "595959"
AZUL = "1F3864"
FONDO = "F2F2F2"
TIPOS_LEGIBLES = {
    "entero": "un número entero",
    "decimal": "un número",
    "fraccion": "una fracción entre 0 y 1, por ejemplo 0,75",
    "porcentaje": "un porcentaje",
    "hora": "una hora HH:MM con su huso",
    "texto": "una palabra o una frase",
}
COLUMNAS_ETIQUETADO = [
    ("Día", 1250),
    ("Sesión", 900),
    ("Decisión", 1350),
    ("Hora", 800),
    ("Entrada", 1150),
    ("SL", 1150),
    ("TP", 1150),
    ("Notas", 1888),
]


# --------------------------------------------------------------------------- XML


def x(texto: object) -> str:
    """Escapa texto para XML y quita los caracteres de control que Word rechaza."""
    s = str(texto).replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    return "".join(c for c in s if c >= " " or c == "\t")


def run(
    texto: str,
    *,
    negrita: bool = False,
    cursiva: bool = False,
    sz: int | None = None,
    color: str | None = None,
) -> str:
    props = ""
    if negrita:
        props += "<w:b/>"
    if cursiva:
        props += "<w:i/>"
    if color:
        props += f'<w:color w:val="{color}"/>'
    if sz:
        props += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
    rpr = f"<w:rPr>{props}</w:rPr>" if props else ""
    return f'<w:r>{rpr}<w:t xml:space="preserve">{x(texto)}</w:t></w:r>'


def parrafo(
    *runs: str,
    estilo: str | None = None,
    sangria: int = 0,
    espacio_antes: int = 0,
    espacio_despues: int = 120,
) -> str:
    props = ""
    if estilo:
        props += f'<w:pStyle w:val="{estilo}"/>'
    props += f'<w:spacing w:before="{espacio_antes}" w:after="{espacio_despues}"/>'
    if sangria:
        props += f'<w:ind w:left="{sangria}"/>'
    return f"<w:p><w:pPr>{props}</w:pPr>{''.join(runs)}</w:p>"


def titulo(texto: str, nivel: int) -> str:
    return parrafo(run(texto), estilo=f"Heading{nivel}")


def texto_simple(texto: str, **kw: Any) -> str:
    return parrafo(run(texto), **kw)


def vineta(texto: str, sz: int | None = None) -> str:
    return parrafo(run(f"•  {texto}", sz=sz), sangria=284, espacio_despues=60)


def _bordes(color: str = "BFBFBF") -> str:
    lados = "".join(
        f'<w:{lado} w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        for lado in ("top", "left", "bottom", "right", "insideH", "insideV")
    )
    return f"<w:tblBorders>{lados}</w:tblBorders>"


def tabla(filas: list[list[str]], anchos: list[int], *, cabecera: bool = True) -> str:
    """Tabla con bordes. Cada celda es una lista de parrafos ya construidos."""
    grid = "".join(f'<w:gridCol w:w="{a}"/>' for a in anchos)
    trs = []
    for n, fila in enumerate(filas):
        celdas = []
        for ancho, contenido in zip(anchos, fila, strict=True):
            fondo = (
                f'<w:shd w:val="clear" w:color="auto" w:fill="{FONDO}"/>'
                if cabecera and n == 0
                else ""
            )
            celdas.append(
                f'<w:tc><w:tcPr><w:tcW w:w="{ancho}" w:type="dxa"/>{fondo}'
                f'<w:vAlign w:val="center"/></w:tcPr>{contenido}</w:tc>'
            )
        repetir = "<w:tblHeader/>" if cabecera and n == 0 else ""
        trs.append(f"<w:tr><w:trPr><w:cantSplit/>{repetir}</w:trPr>{''.join(celdas)}</w:tr>")
    return (
        f'<w:tbl><w:tblPr><w:tblW w:w="{sum(anchos)}" w:type="dxa"/>{_bordes()}'
        '<w:tblCellMar><w:top w:w="60" w:type="dxa"/><w:left w:w="108" w:type="dxa"/>'
        '<w:bottom w:w="60" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar>'
        f"</w:tblPr><w:tblGrid>{grid}</w:tblGrid>{''.join(trs)}</w:tbl>"
        + texto_simple("", espacio_despues=0)  # Word exige un parrafo tras cada tabla
    )


def caja(lineas: int = 3, etiqueta: str = "") -> str:
    """Recuadro vacio para escribir a mano."""
    cuerpo = ""
    if etiqueta:
        cuerpo += parrafo(run(etiqueta, sz=16, color=GRIS), espacio_despues=0)
    cuerpo += "".join(texto_simple("", espacio_despues=0) for _ in range(lineas))
    return tabla([[cuerpo]], [ANCHO], cabecera=False)


# --------------------------------------------------------------------------- documento


def ciudad(huso: str) -> str:
    """El nombre legible de un huso: America/New_York -> New York. Sale del dato, no de aqui."""
    return str(huso).split("/")[-1].replace("_", " ")


def hora_local(iso: str, huso: ZoneInfo) -> str:
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(huso).strftime("%H:%M")


def _cuerpo(
    encabezado: str,
    entrada: dict[str, Any],
    *,
    casos: list[dict[str, Any]] | None = None,
    opciones: list[str] | None = None,
    tipos: list[str] | None = None,
    referencia: str = "",
) -> str:
    """Un bloque de pregunta: que queremos saber, por que, citas, como responder y caja."""
    partes = [titulo(encabezado, 2)]
    partes.append(parrafo(run("Qué queremos saber", negrita=True, color=AZUL), espacio_despues=40))
    partes.append(texto_simple(entrada["pregunta"]))
    partes.append(
        parrafo(
            run("Por qué te lo preguntamos", negrita=True, color=AZUL),
            espacio_antes=80,
            espacio_despues=40,
        )
    )
    partes.append(texto_simple(entrada["porque"]))
    if casos:
        partes.append(
            parrafo(
                run("Lo que dijiste en las grabaciones", negrita=True, color=AZUL),
                espacio_antes=80,
                espacio_despues=40,
            )
        )
        for c in casos:
            cita = " ".join(str(c["cita"]).split())
            if len(cita) > LIMITE_CITA:
                cita = cita[: LIMITE_CITA - 3] + "..."
            partes.append(
                vineta(f"Video {c['video']}, minuto {c['t0']}: \u201c{cita}\u201d", sz=19)
            )
    partes.append(
        parrafo(
            run("Cómo responder", negrita=True, color=AZUL), espacio_antes=80, espacio_despues=40
        )
    )
    partes.append(texto_simple(entrada["respuesta_util"]))
    if opciones:
        partes.append(
            vineta(
                "Opciones previstas: "
                + " / ".join(opciones)
                + ". Si ninguna te encaja, dilo con tus palabras.",
                sz=19,
            )
        )
    if tipos:
        partes.append(vineta("Formato esperado: " + "; ".join(tipos) + ".", sz=19))
    partes.append(caja(3, "Respuesta literal del trader:"))
    if referencia:
        partes.append(
            parrafo(
                run(f"Referencia interna: {referencia}", sz=15, color=GRIS, cursiva=True),
                espacio_despues=240,
            )
        )
    else:
        partes.append(texto_simple("", espacio_despues=240))
    return "".join(partes)


def bloque_extra(e: dict[str, Any], n_total: int) -> str:
    """Pregunta adicional: no nace del registro ni de una ambiguedad, pero tapa un hueco."""
    return _cuerpo(f"{e['id']} de {n_total}. {e['titulo']}", e, referencia=str(e["objetivo"]))


def comprobar_objetivos(ctx_doc: dict[str, Any], sesion: str, repo: Path) -> None:
    """Toda pregunta de la hoja tiene que poder registrarse como feedback despues de la sesion.

    Sin esta comprobacion se puede escribir una pregunta preciosa cuya respuesta no tenga ningun
    objeto al que apuntar, y el hueco solo aparece al intentar registrarla, ya con el trader
    delante. Aqui se cae antes, al generar el documento.
    """
    nombres = set(cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml").parametros)
    evidencias = {i.id for i in cargar_evidencia(repo / "knowledge" / "evidence")}
    declarados = [("precondicion", str(ctx_doc["precondicion"]["objetivo"]))]
    declarados += [(str(e["id"]), str(e["objetivo"])) for e in ctx_doc.get("preguntas_extra") or []]
    for quien, crudo in declarados:
        objetivo = crudo.replace("{sesion}", sesion)
        tipo, _, identificador = objetivo.partition(" ")
        if tipo not in TIPOS_OBJETIVO:
            raise SystemExit(f"{quien}: {tipo!r} no es un tipo de objetivo de feedback")
        if tipo == "parametro" and identificador not in nombres:
            raise SystemExit(
                f"{quien}: el parametro {identificador!r} no esta en el registro, asi que la "
                "respuesta no se podria registrar; anadelo a knowledge/spec/parametros.yaml"
            )
        if tipo == "evidence" and identificador not in evidencias:
            raise SystemExit(f"{quien}: la evidencia {identificador!r} no existe")
        if tipo == "paquete" and identificador != sesion:
            raise SystemExit(f"{quien}: el paquete {identificador!r} no es la sesion {sesion!r}")


def bloque_reafirmaciones(entradas: list[dict[str, Any]], items: dict[str, Any]) -> str:
    """Tabla de confirmacion rapida. El texto sale del item de evidencia, no de este fichero."""
    partes = [titulo("Tercera parte: confirmaciones rápidas", 1)]
    partes.append(
        texto_simple(
            "Esto es lo que hemos entendido de tus grabaciones y que el bot da por bueno. No hace "
            "falta explicarlo otra vez: basta con decir si está bien o corregirlo. Si algo aquí "
            "está mal, es lo más importante que puede salir de esta sesión."
        )
    )
    anchos = [420, 5300, 900, 3018]
    filas = [
        [
            parrafo(run(c, negrita=True, sz=17))
            for c in ("#", "Lo que entendimos", "¿Correcto?", "Corrección")
        ]
    ]
    # El id viene del fichero, NO de la posicion (F12). Numerarlo aqui con `enumerate` hacia que
    # insertar o reordenar una entrada renumerase las catorce en silencio, y el anexo de
    # docs/validation/SESION-01-2026-09-09.md las cita una a una por R-NN: se habria quedado
    # apuntando a otra evidencia sin que nada fallara.
    vistos: set[str] = set()
    for n, e in enumerate(entradas, 1):
        rid = str(e.get("id") or "")
        if not re.fullmatch(r"R-\d{2}", rid, re.ASCII):
            raise SystemExit(
                f"reafirmacion {n}: 'id' invalido {rid!r}; va un R-NN explicito en "
                "contexto_preguntas.yaml"
            )
        if rid in vistos:
            raise SystemExit(f"reafirmacion {n}: id repetido {rid}")
        vistos.add(rid)
        item = items.get(e["evidencia"])
        if item is None:
            raise SystemExit(
                f"{rid}: la evidencia {e['evidencia']} no existe; corrige contexto_preguntas.yaml"
            )
        celda = parrafo(run(item.afirmacion, sz=18))
        celda += parrafo(
            run(
                f"Video {item.video_id}, minuto {item.t0}. Importa porque {e['nota']}.",
                sz=15,
                color=GRIS,
                cursiva=True,
            ),
            espacio_despues=0,
        )
        filas.append(
            [
                parrafo(run(rid, sz=17)),
                celda,
                parrafo(run("", sz=17)),
                parrafo(run("", sz=17)),
            ]
        )
    partes.append(tabla(filas, anchos))
    return "".join(partes)


def bloque_cierre(puntos: list[str]) -> str:
    """Lo que se verifica antes de dar la sesion por cerrada."""
    partes = [titulo("Cierre de la sesión", 1)]
    partes.append(
        texto_simple(
            "Antes de despedirse, repasar esta lista. Lo que quede sin marcar se anota abajo con "
            "su motivo: un hueco declarado es manejable, un hueco olvidado no."
        )
    )
    filas = [[parrafo(run("[   ]", sz=18)), parrafo(run(p, sz=18))] for p in puntos]
    partes.append(tabla(filas, [700, 8938], cabecera=False))
    for etiqueta, lineas in (
        ("Preguntas que quedan sin cerrar, y por qué:", 3),
        ("Dudas nuevas que han salido hoy:", 4),
        ("Compromisos y fecha de la siguiente sesión:", 2),
    ):
        partes.append(
            parrafo(run(etiqueta, negrita=True, color=AZUL), espacio_antes=120, espacio_despues=40)
        )
        partes.append(caja(lineas))
    return "".join(partes)


def bloque_pregunta(p: dict[str, Any], ctx: dict[str, Any], n_total: int) -> str:
    origen = next((o for o in p["origenes"] if o["tipo"] == "ambiguedad"), p["origenes"][0])
    entrada = ctx.get(origen["id"])
    if entrada is None:
        raise SystemExit(
            f"{p['id']}: falta el contexto de {origen['id']!r} en contexto_preguntas.yaml "
            "(anadelo antes de generar la hoja)"
        )
    marca = "   [BLOQUEANTE]" if p["bloqueante"] else ""
    encabezado = str(entrada.get("titulo") or p["titulo"])
    return _cuerpo(
        f"{p['id']} de {n_total}. {encabezado}{marca}",
        entrada,
        casos=p["casos"],
        opciones=p["respuesta_esperada"].get("opciones"),
        tipos=[TIPOS_LEGIBLES.get(x, x) for x in p["respuesta_esperada"].get("tipos") or []],
        referencia=", ".join(f"{o['tipo']} {o['id']}" for o in p["origenes"]),
    )


def bloque_etiquetado(
    casos: list[dict[str, Any]],
    asignacion: dict[str, str],
    config: Any,
    huso: ZoneInfo,
    ref_anclaje: str,
) -> str:
    dev = sorted((c for c in casos if asignacion.get(c["id"]) == "dev"), key=lambda c: c["dia"])
    anclaje = next(a for a in config.anclajes if a.coincide_con_sesiones)
    rejillas = {
        tuple(hora_local(t, huso) for t in c["limites_h4"].get(anclaje.etiqueta, [])) for c in dev
    }
    if not dev:
        raise SystemExit(
            "el paquete no tiene ningun caso en la particion dev: la hoja no tendria nada que "
            "etiquetar; revisa los cupos de config.yaml"
        )
    partes = [titulo("Cuarta parte: etiquetado de los días", 1)]
    partes.append(
        texto_simple(
            f"Son {len(dev)} días de EURUSD que, según lo que has confirmado al principio de esta "
            "hoja, no has visto. Ábrelos en replay uno a uno y, "
            "para cada una de tus dos sesiones, dinos qué habrías hecho: comprar, vender o no "
            "operar. "
            "Si operas, apunta la hora de entrada, el precio de entrada, el stop y el objetivo. "
            "Importante: decide como decidirías en directo, sin adelantar el gráfico para ver cómo "
            "acabó el día."
        )
    )
    sesiones = ", ".join(f"{s.nombre} de {s.desde} a {s.hasta}" for s in config.sesiones)
    partes.append(
        vineta(
            f"Gráfico que verás: de {config.ventana_local[0]} a {config.ventana_local[1]}, "
            "hora tuya, para que tengas contexto de la madrugada. Lo que etiquetas son solo tus "
            f"dos sesiones: {sesiones}."
        )
    )
    if len(rejillas) == 1:
        horas = " · ".join(next(iter(rejillas)))
        partes.append(
            vineta(
                f"Suponiendo que tu gráfico empieza la vela de 4 horas a las {anclaje.hora} de "
                f"la hora de {ciudad(anclaje.huso)}, que es lo que creemos, en todos estos "
                f"días tus velas de 4 horas abrirían a: {horas}. Es una suposición nuestra, y es "
                f"justo lo que confirmas en la pregunta {ref_anclaje}."
            )
        )
    partes.append(vineta("Decisión: " + " / ".join(config.etiquetas) + "."))
    partes.append(texto_simple(""))
    cab = [parrafo(run(t, negrita=True, sz=17)) for t, _ in COLUMNAS_ETIQUETADO]
    filas = [cab]
    for c in dev:
        for k, s in enumerate(config.sesiones):
            fila = [parrafo(run(c["dia"] if k == 0 else "", sz=17))]
            fila.append(parrafo(run(s.nombre, sz=17)))
            fila += [parrafo(run("", sz=17)) for _ in range(len(COLUMNAS_ETIQUETADO) - 2)]
            filas.append(fila)
    partes.append(tabla(filas, [a for _, a in COLUMNAS_ETIQUETADO]))
    partes.append(
        texto_simple(
            "Si prefieres grabar la pantalla mientras los recorres, mucho mejor: con que digas la "
            "fecha en voz alta antes de cada día, nosotros sacamos las decisiones de la grabación.",
            espacio_antes=120,
        )
    )
    return "".join(partes)


def numero_de_pregunta(preguntas: list[dict[str, Any]], origen: str) -> str:
    """El `P-NN` que le toco a un origen en ESTE paquete.

    `kit build` renumera las preguntas cada vez, asi que escribir un `P-03` a mano en el texto
    de la hoja es una referencia que se rompe en silencio al cambiar el cuestionario.
    """
    for p in preguntas:
        if any(o["id"] == origen for o in p["origenes"]):
            return str(p["id"])
    raise SystemExit(f"ninguna pregunta del paquete nace de {origen!r}; revisa el cuestionario")


def documento(repo: Path, sesion: str) -> str:
    cuestionario, ventanas, particiones = esquema_paquete(repo, sesion)
    config = cargar_config(repo / DIRECTORIO_KIT / "config.yaml")
    ctx_doc = cargar_yaml(
        (repo / DIRECTORIO_KIT / "contexto_preguntas.yaml").read_text(encoding="utf-8")
    )
    registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    huso = ZoneInfo(registro.texto("huso_operativa"))
    casos = ventanas["casos"]
    meses = sorted({str(c["dia"])[:7] for c in casos})
    preguntas = cuestionario["preguntas"]
    # Numeros y recuentos derivados del paquete: escribirlos a mano en el texto de la hoja los
    # deja apuntando a otra pregunta en cuanto `kit build` renumera.
    ref_anclaje = numero_de_pregunta(preguntas, ANCLAJE_H4)
    bloqueantes = [str(p["id"]) for p in preguntas if p["bloqueante"]]

    partes = [titulo("Sesión 1 con el trader. Hoja de respuestas", 1)]
    n_dev = sum(1 for c in casos if particiones["asignacion"].get(c["id"]) == "dev")
    partes.append(
        texto_simple(
            f"Paquete {sesion}. {len(preguntas)} preguntas del cuestionario, "
            f"{len(ctx_doc.get('preguntas_extra') or [])} preguntas adicionales, "
            f"{len(ctx_doc.get('reafirmaciones') or [])} confirmaciones rápidas y {n_dev} días "
            "para etiquetar. Esta hoja se rellena durante la sesión y la sesión se graba en vídeo."
        )
    )
    partes.append(
        tabla(
            [
                [parrafo(run(a, negrita=True, sz=18))] + [parrafo(run("", sz=18))]
                for a in (
                    "Fecha real de la sesión",
                    "Participantes",
                    "Fichero de la grabación",
                    "Quién anota",
                )
            ],
            [3200, 6438],
            cabecera=False,
        )
    )

    partes.append(titulo("Cómo se usa esta hoja", 2))
    for t in (
        "Cada pregunta trae lo que el trader dijo en las grabaciones. Se le lee, se le pregunta y "
        "se apunta su respuesta con SUS palabras, no un resumen.",
        "Antes de cada pregunta, di en voz alta su número (por ejemplo, vamos con la P cero uno). "
        "Así se localiza después en el vídeo sin buscar a ciegas.",
        f"Estas están marcadas como bloqueantes: {', '.join(bloqueantes)}. Si no se cierran, el "
        "resto del trabajo se queda parado. Van primero a propósito.",
        "Si una respuesta abre una duda nueva, apúntala igual. Una duda registrada vale más que "
        "una regla inventada.",
        f"La pregunta {ref_anclaje} necesita además una captura de pantalla de la configuración "
        "del gráfico.",
        "Las citas están tal como las transcribió el sistema desde el audio. Si alguna está mal "
        "transcrita, que lo diga: también es un dato y se corrige.",
    ):
        partes.append(vineta(t))

    notas = ctx_doc.get("notas_para_el_trader") or []
    if notas:
        partes.append(titulo("Lo que le decimos al trader antes de empezar", 2))
        for n in notas:
            partes.append(vineta(n))

    comprobar_objetivos(ctx_doc, sesion, repo)

    prec = ctx_doc["precondicion"]
    partes.append(titulo(f"Antes de empezar. {prec['titulo']}", 1))
    partes.append(parrafo(run("Qué queremos saber", negrita=True, color=AZUL), espacio_despues=40))
    partes.append(texto_simple(prec["pregunta"].replace("{meses}", " y ".join(meses))))
    partes.append(
        parrafo(
            run("Por qué te lo preguntamos", negrita=True, color=AZUL),
            espacio_antes=80,
            espacio_despues=40,
        )
    )
    partes.append(texto_simple(prec["porque"]))
    partes.append(
        parrafo(
            run("Cómo responder", negrita=True, color=AZUL), espacio_antes=80, espacio_despues=40
        )
    )
    partes.append(texto_simple(prec["respuesta_util"]))
    partes.append(caja(2, "Respuesta literal del trader:"))
    partes.append(
        parrafo(
            run(
                "Referencia interna: " + str(prec["objetivo"]).replace("{sesion}", sesion),
                sz=15,
                color=GRIS,
                cursiva=True,
            ),
            espacio_despues=240,
        )
    )

    partes.append(titulo("Primera parte: preguntas", 1))
    for p in preguntas:
        partes.append(bloque_pregunta(p, ctx_doc["preguntas"], len(preguntas)))

    extras = ctx_doc.get("preguntas_extra") or []
    if extras:
        partes.append(titulo("Segunda parte: preguntas adicionales", 1))
        partes.append(
            texto_simple(
                "Estas no salen de una contradicción en tus grabaciones, sino de cosas que el bot "
                "necesita decidir y sobre las que nunca hemos hablado. Si no las cerramos, las "
                "decidiríamos nosotros por ti."
            )
        )
        for e in extras:
            partes.append(bloque_extra(e, len(extras)))

    reafirmaciones = ctx_doc.get("reafirmaciones") or []
    if reafirmaciones:
        items = {i.id: i for i in cargar_evidencia(repo / "knowledge" / "evidence")}
        partes.append(bloque_reafirmaciones(reafirmaciones, items))

    partes.append(bloque_etiquetado(casos, particiones["asignacion"], config, huso, ref_anclaje))
    if ctx_doc.get("cierre"):
        partes.append(bloque_cierre(list(ctx_doc["cierre"])))
    cuerpo = "".join(partes)
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{cuerpo}"
        '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" '
        'w:header="709" w:footer="709" w:gutter="0"/></w:sectPr></w:body></w:document>'
    )


ESTILOS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    "<w:docDefaults><w:rPrDefault><w:rPr>"
    '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>'
    '<w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="es-ES"/>'
    "</w:rPr></w:rPrDefault><w:pPrDefault><w:pPr>"
    '<w:spacing w:after="120" w:line="276" w:lineRule="auto"/>'
    "</w:pPr></w:pPrDefault></w:docDefaults>"
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
    '<w:name w:val="Normal"/><w:qFormat/></w:style>'
    + "".join(
        f'<w:style w:type="paragraph" w:styleId="Heading{n}">'
        f'<w:name w:val="heading {n}"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>'
        f"<w:qFormat/><w:pPr><w:keepNext/>"
        f'<w:spacing w:before="{antes}" w:after="120"/>'
        f'<w:outlineLvl w:val="{n - 1}"/></w:pPr>'
        f'<w:rPr><w:b/><w:color w:val="{AZUL}"/><w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>'
        "</w:style>"
        for n, sz, antes in ((1, 32, 360), (2, 26, 280), (3, 23, 200))
    )
    + "</w:styles>"
)
CONTENT_TYPES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.'
    'relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-'
    'officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-'
    'officedocument.wordprocessingml.styles+xml"/></Types>'
)
RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
    'relationships/officeDocument" Target="word/document.xml"/></Relationships>'
)
RELS_DOC = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
    'relationships/styles" Target="styles.xml"/></Relationships>'
)


def escribir_docx(ruta: Path, document_xml: str) -> None:
    if ruta.is_dir():
        raise SystemExit(f"{ruta} es una carpeta; --salida quiere la ruta de un fichero .docx")
    try:
        _escribir(ruta, document_xml)
    except PermissionError as exc:
        raise SystemExit(
            f"no se puede escribir {ruta.name}: seguramente esta abierto en Word. "
            "Cierralo y repite el comando."
        ) from exc
    except FileNotFoundError as exc:
        raise SystemExit(f"no existe la carpeta {ruta.parent}; creala o cambia --salida") from exc
    except OSError as exc:
        raise SystemExit(f"no se puede escribir {ruta}: {exc}") from exc


def _escribir(ruta: Path, document_xml: str) -> None:
    with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/document.xml", document_xml)
        z.writestr("word/_rels/document.xml.rels", RELS_DOC)
        z.writestr("word/styles.xml", ESTILOS)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sesion", help="AAAA-MM-DD-sesion-NN (por defecto, la unica del kit)")
    ap.add_argument("--salida", help="ruta del .docx (por defecto, en la raiz del repositorio)")
    args = ap.parse_args()
    sesiones = sesiones_del_kit(RAIZ)
    if not sesiones:
        print("ERROR: no hay ningun paquete en knowledge/cases/kit/", file=sys.stderr)
        return 1
    sesion = args.sesion or sesiones[-1]
    if sesion not in sesiones:
        print(f"ERROR: no existe el paquete {sesion} (hay {sesiones})", file=sys.stderr)
        return 1
    salida = (
        Path(args.salida)
        if args.salida
        else RAIZ / f"Sesion 1 - hoja de respuestas ({sesion}).docx"
    )
    try:
        xml = documento(RAIZ, sesion)
    except SystemExit:
        raise
    except (ValueError, LookupError, OSError, AttributeError, TypeError) as exc:
        # El contexto y el paquete son ficheros que se editan a mano: un `porque` que falta o un
        # YAML mal indentado tienen que salir como un error legible, no como un traceback.
        print(
            f"ERROR: no se puede componer la hoja de {sesion}: {type(exc).__name__}: {exc}. "
            "Revisa knowledge/cases/kit/contexto_preguntas.yaml y el paquete.",
            file=sys.stderr,
        )
        return 1
    escribir_docx(salida, xml)
    print(f"OK: {salida}")
    print(
        "Recuerda: si vuelves a ejecutar `kit build`, esta hoja se queda vieja. Regenerala "
        "siempre como ultimo paso antes de imprimir."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit as salida_:
        if isinstance(salida_.code, str):  # los avisos del generador, con el mismo formato
            print(f"ERROR: {salida_.code}", file=sys.stderr)
            raise SystemExit(1) from None
        raise
