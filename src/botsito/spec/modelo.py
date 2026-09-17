"""Carga estricta de la StrategySpec y del glosario (F11, ADR-0013).

Una regla no lleva numeros: nombra parametros del registro y el valor lo pone el registro, que es
la unica puerta (ADR-0002). Lo que si lleva es la frase del trader que la sostiene, y esa frase
tiene que coincidir con el registro de feedback que declara: si alguien la retoca para que "quede
mejor", la comprobacion falla. Es la misma idea que ADR-0009 aplica a la evidencia.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from botsito.comun import ids
from botsito.comun.yaml_estricto import YamlError, leer_yaml
from botsito.evidence.verificacion import CitaError, buscar_secuencia, tokens, trozos_de_cita

FICHERO_SPEC = "knowledge/spec/strategy_spec.yaml"
FICHERO_GLOSARIO = "knowledge/spec/glossary.yaml"

ESTADOS_REGLA = ("VIGENTE", "DESCARTADA")
# La precedencia entre reglas va por CLASE y no por orden del fichero (ADR-0018). El orden es
# EDITORIAL -agrupado por tema, con comentarios, y RN-026/RN-027 viven bajo la cabecera "reglas
# descartadas" siendo VIGENTES-, asi que tomarlo por semantica convertia un reagrupamiento
# cosmetico en un cambio de comportamiento. De mas fuerte a mas debil.
CLASES_REGLA = ("gate", "terminal", "disparador", "fallback")
CAMPOS_REGLA = {
    "id",
    "titulo",
    "cuando",
    "entonces",
    "parametros",
    "cita",
    "literal",
    "clase",
    "estado",
}
CAMPOS_REGLA_OPCIONALES = {"notas", "decision", "complementa", "forma"}
CAMPOS_TERMINO = {"termino", "definicion", "cita", "literal"}
CAMPOS_TERMINO_OPCIONALES = {"alias", "visto_en"}

# Un campo ejecutable no puede llevar un valor de negocio: el valor vive en el registro y aqui
# solo va el nombre del parametro. Basta con exigir que ninguna cifra empiece una palabra: asi
# `M15`, `H4` y `liquidez_m15_criterio_toma` pasan -son nombres, no valores- y `0,8` o `15:00`
# no. El lookbehind excluye tambien los digitos, o el `5` de `m15` contaria por su cuenta.
_CIFRA = re.compile(r"(?<![A-Za-z_0-9])\d")

# Y en letras, que es la via de escape obvia: "el stop va al ochenta por ciento de la caja"
# pasaria la comprobacion de cifras y seria el mismo problema. Pero un numero en letras solo es
# un VALOR cuando trae unidad: "se abre una operacion" o "los dos esquemas" son espanol, no
# parametros, y prohibirlos haria imposible escribir una regla. Por eso se exige la pareja
# numero + unidad, y `horas` queda fuera porque `vela de cuatro horas` es una temporalidad.
_NUMEROS_EN_LETRAS = (
    "cero",
    "uno",
    "una",
    "un",
    "dos",
    "tres",
    "cuatro",
    "cinco",
    "seis",
    "siete",
    "ocho",
    "nueve",
    "diez",
    "once",
    "doce",
    "quince",
    "veinte",
    "veinticinco",
    "treinta",
    "cuarenta",
    "cincuenta",
    "sesenta",
    "setenta",
    "ochenta",
    "noventa",
    "cien",
    "ciento",
    "mil",
    "medio",
    "media",
    "mitad",
    "cuarto",
    "tercio",
    "doble",
    "triple",
)
_UNIDADES = (
    "por ciento",
    "porciento",
    "cartuchos?",
    "intentos?",
    "pips?",
    "puntos?",
    "lotes?",
    "veces",
    "minutos?",
    "por mil",
    # Sustantivos de dominio, anadidos en la auditoria del 2026-09-10. El comentario de arriba
    # declaraba que "se abre una operacion" y "los dos esquemas" eran espanol y no parametros;
    # eran DOS CARDINALIDADES DE NEGOCIO viviendo fuera del registro, en RN-018 y RN-009. Ahora
    # son `operaciones_simultaneas_max` y `zonas_control_max_por_esquema`.
    "zonas?",
    "esquemas?",
    "operacion(?:es)?",
    "cartuchos?",
)
# En LOS DOS ORDENES, y admitiendo hasta dos palabras en medio. La auditoria del 2026-09-10
# encontro que esto solo casaba numero+unidad SEGUIDOS, asi que "las operaciones abiertas son
# cero" pasaba -y esa frase la escribi yo, arreglando justamente este fallo- igual que "hay una
# unica operacion abierta". Un valor de negocio no deja de serlo por el orden de las palabras.
_NUM = "(?:" + "|".join(_NUMEROS_EN_LETRAS) + ")"
_UNI = "(?:" + "|".join(_UNIDADES) + ")"
_HUECO = r"(?:\s+\w+){0,2}"
# La rama invertida admite UNA sola palabra en medio, no dos: con dos, "el lote calculado no es un
# multiplo de instrumento_lote_paso" saltaba por "lote … no es un", que es espanol corriente.
_HUECO_INV = r"(?:\s+\w+)?"
_EN_LETRAS = re.compile(
    r"\b(?:"
    + _NUM
    + _HUECO
    + r"\s+"
    + _UNI
    + r"|"
    + _UNI
    + _HUECO_INV
    + r"\s+(?:son|es|de)\s+"
    + _NUM
    + r")\b",
    re.IGNORECASE,
)


def _cifra_de_negocio(texto: str) -> str | None:
    """El primer valor de negocio del texto -en cifra o en letra-, o None si solo hay nombres."""
    m = _CIFRA.search(texto)
    if m:
        return m.group(0)
    m = _EN_LETRAS.search(texto)
    return m.group(0) if m else None


class SpecError(ValueError):
    """La spec no cumple su esquema o cita algo que no existe."""


@dataclass(frozen=True, slots=True)
class Regla:
    id: str
    titulo: str
    cuando: str
    entonces: str
    parametros: tuple[str, ...]
    cita: str
    literal: str
    estado: str
    clase: str = "disparador"
    notas: str | None = None
    # El ADR que sostiene lo que la regla decide POR SU CUENTA. Obligatorio cuando la regla opera
    # sobre parametros de entorno: ahi no hay trader al que citar, hay una decision nuestra.
    decision: str | None = None
    # Otra regla a la que esta REFINA en vez de competir con ella: un invariante, o el mismo
    # efecto dicho para otro caso. Sin este campo, dos reglas que se solapan a proposito son
    # indistinguibles de dos que se pisan por accidente.
    complementa: tuple[str, ...] = ()
    # La forma ejecutable (F12, ADR-0019). `None` mientras la regla siga en prosa: el piloto son
    # cuatro, y `spec status` dice cuantas faltan en vez de fingir que estan todas.
    forma: Any | None = None

    @property
    def vigente(self) -> bool:
        return self.estado == "VIGENTE"


@dataclass(frozen=True, slots=True)
class Termino:
    termino: str
    definicion: str
    cita: str
    literal: str
    alias: tuple[str, ...] = ()
    visto_en: str | None = None


def _texto(doc: dict[str, Any], campo: str, origen: str) -> str:
    v = doc.get(campo)
    if not isinstance(v, str) or not v.strip():
        raise SpecError(f"{origen}: falta '{campo}'")
    return " ".join(v.split())


def _campos(doc: dict[str, Any], obligatorios: set[str], opcionales: set[str], origen: str) -> None:
    faltan = obligatorios - set(doc)
    if faltan:
        raise SpecError(f"{origen}: faltan campos {sorted(faltan)}")
    sobran = set(doc) - obligatorios - opcionales
    if sobran:
        raise SpecError(f"{origen}: campos desconocidos {sorted(map(str, sobran))}")


def _cita_valida(cita: str) -> bool:
    return ids.es_id_de("evidence", cita) or ids.es_id_de("feedback", cita)


def cargar_reglas(ruta: Path) -> list[Regla]:
    try:
        doc = leer_yaml(ruta)
    except (OSError, YamlError) as exc:
        raise SpecError(f"{ruta.name}: {exc}") from exc
    esperadas = {
        "version_esquema",
        "reglas",
        "predicados",
        "acciones",
        "efectos",
        "hechos",
        "acumuladores",
        "tokens",
    }
    if not isinstance(doc, dict) or not {"version_esquema", "reglas"} <= set(doc) <= esperadas:
        raise SpecError(f"{ruta.name}: se esperan {sorted(esperadas)}")
    if doc["version_esquema"] != 3:
        raise SpecError(f"{ruta.name}: version_esquema desconocida {doc['version_esquema']!r}")
    bruto = doc["reglas"]
    if not isinstance(bruto, list) or not bruto:
        raise SpecError(f"{ruta.name}: 'reglas' debe ser una lista no vacia")

    reglas: list[Regla] = []
    vistos: set[str] = set()
    for i, r in enumerate(bruto, start=1):
        origen = f"{ruta.name}: regla {i}"
        if not isinstance(r, dict):
            raise SpecError(f"{origen}: no es un mapa")
        _campos(r, CAMPOS_REGLA, CAMPOS_REGLA_OPCIONALES, origen)
        rid = str(r["id"])
        if not ids.es_id_de("regla", rid):
            raise SpecError(f"{origen}: id {rid!r} no tiene formato RN-NNN")
        if rid in vistos:
            raise SpecError(f"{origen}: id repetido {rid}")
        vistos.add(rid)
        estado = str(r["estado"])
        if estado not in ESTADOS_REGLA:
            raise SpecError(f"{rid}: estado {estado!r} no esta en {ESTADOS_REGLA}")
        clase = str(r["clase"])
        if clase not in CLASES_REGLA:
            raise SpecError(f"{rid}: clase {clase!r} no esta en {CLASES_REGLA}")
        params = r["parametros"]
        if not isinstance(params, list) or not all(
            isinstance(p, str) and p.strip() for p in params
        ):
            raise SpecError(f"{rid}: 'parametros' debe ser una lista de nombres")
        cita = str(r["cita"])
        if not _cita_valida(cita):
            raise SpecError(f"{rid}: cita {cita!r} no es un id de evidencia ni de feedback")
        comp = r.get("complementa") or []
        if not isinstance(comp, list) or not all(ids.es_id_de("regla", str(c)) for c in comp):
            raise SpecError(f"{rid}: 'complementa' debe ser una lista de ids RN-NNN")
        decision = r.get("decision")
        if decision is not None and not re.fullmatch(r"ADR-\d{4}", str(decision), re.ASCII):
            raise SpecError(f"{rid}: decision {decision!r} no tiene formato ADR-NNNN")
        for campo in ("cuando", "entonces"):
            texto = _texto(r, campo, rid)
            cifra = _cifra_de_negocio(texto)
            if cifra is not None:
                raise SpecError(
                    f"{rid}: '{campo}' contiene la cifra {cifra!r}; el valor vive en el registro "
                    f"y aqui solo va el nombre del parametro"
                )
        reglas.append(
            Regla(
                id=rid,
                titulo=_texto(r, "titulo", rid),
                cuando=_texto(r, "cuando", rid),
                entonces=_texto(r, "entonces", rid),
                parametros=tuple(params),
                cita=cita,
                literal=_texto(r, "literal", rid),
                estado=estado,
                clase=clase,
                notas=" ".join(str(r["notas"]).split()) if r.get("notas") else None,
                decision=str(r["decision"]).strip() if r.get("decision") else None,
                complementa=tuple(str(c).strip() for c in comp),
                forma=r.get("forma"),
            )
        )
    return reglas


def cargar_glosario(ruta: Path) -> list[Termino]:
    try:
        doc = leer_yaml(ruta)
    except (OSError, YamlError) as exc:
        raise SpecError(f"{ruta.name}: {exc}") from exc
    if not isinstance(doc, dict) or set(doc) != {"terminos"}:
        raise SpecError(f"{ruta.name}: se espera una unica clave 'terminos'")
    bruto = doc["terminos"]
    if not isinstance(bruto, list) or not bruto:
        raise SpecError(f"{ruta.name}: 'terminos' debe ser una lista no vacia")
    terminos: list[Termino] = []
    vistos: set[str] = set()
    for i, t in enumerate(bruto, start=1):
        origen = f"{ruta.name}: termino {i}"
        if not isinstance(t, dict):
            raise SpecError(f"{origen}: no es un mapa")
        _campos(t, CAMPOS_TERMINO, CAMPOS_TERMINO_OPCIONALES, origen)
        nombre = _texto(t, "termino", origen)
        if nombre.casefold() in vistos:
            raise SpecError(f"{origen}: termino repetido {nombre!r}")
        vistos.add(nombre.casefold())
        cita = str(t["cita"])
        if not _cita_valida(cita):
            raise SpecError(f"{nombre}: cita {cita!r} no es un id de evidencia ni de feedback")
        alias = t.get("alias") or []
        if not isinstance(alias, list) or not all(isinstance(a, str) and a.strip() for a in alias):
            raise SpecError(f"{nombre}: 'alias' debe ser una lista de textos")
        terminos.append(
            Termino(
                termino=nombre,
                definicion=_texto(t, "definicion", nombre),
                cita=cita,
                literal=_texto(t, "literal", nombre),
                alias=tuple(" ".join(a.split()) for a in alias),
                visto_en=" ".join(str(t["visto_en"]).split()) if t.get("visto_en") else None,
            )
        )
    return terminos


def literal_coincide(literal: str, texto_citado: str) -> bool:
    """Si el `literal` de una regla esta de verdad en el texto que la regla cita.

    Mismo criterio que ADR-0009 usa con la evidencia: se comparan TOKENS normalizados, no cadenas,
    y el comodin `[...]` permite saltar lo de en medio. Asi una regla no puede afirmar que el
    trader dijo algo que no dijo, ni suavizar sus palabras para que encajen mejor.
    """
    try:
        trozos = trozos_de_cita(literal)
    except CitaError:
        return False
    return bool(buscar_secuencia(tokens(texto_citado), trozos))


def comprobar_literales(
    reglas: list[Regla],
    textos: dict[str, str],
    terminos: list[Termino] | None = None,
    vocabulario: Mapping[str, Mapping[str, Any]] | None = None,
) -> list[str]:
    """Cada regla y cada termino dicen lo que dice su cita, o se nombra el problema.

    `textos` es cita_id -> lo que se dijo (respuesta del trader o cita de la evidencia). El
    glosario entra aqui desde la auditoria del 2026-09-09, que encontro ocho definiciones que
    decian mas que su cita o citaban otra cosa, sin que nada lo vigilara.
    """
    problemas: list[str] = []
    for termino in terminos or []:
        citado_t = textos.get(termino.cita)
        if citado_t is not None and not literal_coincide(termino.literal, citado_t):
            problemas.append(
                f"glosario {termino.termino!r}: su literal no aparece en {termino.cita}"
            )
    for r in reglas:
        citado = textos.get(r.cita)
        if citado is None:
            # Que la cita exista lo comprueba `comprobar_contra`, asi que aqui saltarsela es
            # correcto: si no existe, ya lo denuncia aquella.
            continue
        if not literal_coincide(r.literal, citado):
            problemas.append(
                f"{r.id}: su literal no aparece en {r.cita}; una regla no puede decir algo "
                f"distinto de lo que cita"
            )
    # El vocabulario de F12 tambien lleva `cita` y `literal` propios, y nadie los cruzaba: el
    # comentario que habia aqui predijo exactamente eso -"el dia que algo con cita propia no pase
    # por comprobar_contra, esta guardia se apagaria sin avisar"- y es lo que paso. Se podia poner
    # cualquier frase en boca del trader dentro de un predicado (auditoria de cierre de F12).
    for seccion in ("predicados", "acciones", "hechos", "acumuladores"):
        for nombre, datos in sorted((vocabulario or {}).get(seccion, {}).items()):
            if not isinstance(datos, dict) or not datos.get("cita") or not datos.get("literal"):
                continue
            citado_v = textos.get(str(datos["cita"]))
            if citado_v is not None and not literal_coincide(str(datos["literal"]), citado_v):
                problemas.append(f"{seccion} '{nombre}': su literal no aparece en {datos['cita']}")
    return problemas


def comprobar_contra(
    reglas: list[Regla],
    terminos: list[Termino],
    parametros: set[str],
    citas_conocidas: set[str],
    vocabulario: Mapping[str, Mapping[str, Any]] | None = None,
) -> list[str]:
    """Que cada regla nombre parametros que existen y cite algo que existe.

    El vocabulario entra desde la auditoria de cierre de F12: predicados y acumuladores llevan
    `cita` propia desde ADR-0019 y nadie comprobaba que existiera, asi que un `fb-...-deadbeef`
    pasaba entero.
    """
    problemas: list[str] = []
    for r in reglas:
        for p in r.parametros:
            if p not in parametros:
                problemas.append(f"{r.id}: nombra el parametro {p!r}, que no esta en el registro")
        if r.cita not in citas_conocidas:
            problemas.append(f"{r.id}: cita {r.cita}, que no existe")
    for t in terminos:
        if t.cita not in citas_conocidas:
            problemas.append(f"glosario {t.termino!r}: cita {t.cita}, que no existe")
    for seccion in ("predicados", "acciones", "hechos", "acumuladores"):
        for nombre, datos in sorted((vocabulario or {}).get(seccion, {}).items()):
            cita_v = datos.get("cita") if isinstance(datos, dict) else None
            if cita_v not in (None, "") and str(cita_v) not in citas_conocidas:
                problemas.append(f"{seccion} '{nombre}': cita {cita_v}, que no existe")
    return problemas


def comprobar_decisiones(
    reglas: list[Regla], fuentes: Mapping[str, str], ids_adr: set[str]
) -> list[str]:
    """Una regla que opera sobre parametros de ENTORNO declara el ADR que la decide.

    `comprobar_literales` mira que el literal este de verdad en la cita, pero no puede mirar que la
    regla no diga MAS que su literal: eso no es mecanizable en general. Lo que si es mecanizable es
    el caso que importa. Un parametro cuya `fuente` es `decision` no lo dijo el trader -es la ficha
    del simbolo, el reloj del servidor, la cuenta-, asi que una regla construida sobre el esta
    decidiendo algo por su cuenta, y su `cita` del trader no puede sostenerlo.

    Lo encontro la auditoria del 2026-09-10 con dos reglas reales: RN-026 decidia abstenerse cuando
    el broker no admite el stop, y RN-027 redondear el lotaje a la baja. Ninguna de las dos cosas
    esta en su literal; las dos citaban frases genericas del trader y pasaban la comprobacion.

    `fuentes` es nombre de parametro -> tipo de fuente ("evidence" | "feedback" | "decision").
    """
    problemas: list[str] = []
    for r in reglas:
        # Tambien las DESCARTADAS: una regla descartada sigue afirmando algo -por que se descarto-
        # y su `decision` entra en el hash. Solo se le exige que el ADR exista, no que lo declare.
        if r.decision is not None and r.decision not in ids_adr:
            problemas.append(f"{r.id}: decision {r.decision}, que no existe")
            continue
        if not r.vigente:
            continue
        de_entorno = sorted(p for p in r.parametros if fuentes.get(p) == "decision")
        if de_entorno and r.decision is None:
            problemas.append(
                f"{r.id}: opera sobre {', '.join(de_entorno)}, que no los dijo el trader sino un "
                f"ADR; una regla asi decide algo por su cuenta y tiene que declarar 'decision'"
            )
    return problemas


def comprobar_precedencia(reglas: list[Regla]) -> list[str]:
    """Que la precedencia no dependa del orden del fichero, y que no haya empates ciegos.

    El orden de `strategy_spec.yaml` es EDITORIAL: esta agrupado por tema, con comentarios, y
    RN-026 y RN-027 viven bajo la cabecera "reglas descartadas" siendo VIGENTES. Tomarlo por
    semantica daba la respuesta equivocada en tres pares reales, encontrados el 2026-09-10:

    - RN-006 (id 006) ganaba a RN-014 (014) y a RN-018 (018): con una operacion abierta el bot
      reubicaba una orden limite en paralelo en vez de poner el break even.
    - RN-019 (019) ganaba a RN-020 (020): se reentraba despues de tocar el tope diario.
    - RN-022 es la clausula `else` y estaba ANTES de RN-026 y RN-027, que son reglas reales.

    Por eso la precedencia va por `clase` (ADR-0018).

    LO QUE ESTA FUNCION NO HACIA: cazar ninguno de esos tres pares. Decidir que dos reglas actuan
    "sobre el mismo evento" exigia leer `cuando`, que entonces era prosa. Desde que las 24
    vigentes tienen `forma`, ya no: se comparan los disparadores EJECUTABLES, y ahi aparecio un
    par que llevaba dias escondido -RN-013 y RN-015, las dos `disparador`, con el `forma.cuando`
    identico byte a byte y sin `complementa` entre ellas-.

    Lo que si comprueba, que es poco pero es cierto: que haya exactamente un `fallback`; que dos
    reglas de la misma clase no tengan exactamente los mismos parametros (un clon); y que los
    parametros de una no sean un SUBCONJUNTO de los de otra de su clase, que es la forma en que
    RN-017 se solapa con RN-016 y RN-013 con RN-011.
    """
    problemas: list[str] = []
    vigentes = [r for r in reglas if r.vigente]

    # `complementa` es lo que exime de las denuncias de abajo, y solo se validaba su FORMATO: un
    # `RN-777` o una regla DESCARTADA -que ya no refina nada- apagaban la guardia igual que una
    # declaracion cierta (revision de diseno de la rama de fidelidad, 2026-09-16).
    por_id_todas = {r.id: r for r in reglas}
    for r in reglas:
        for c in r.complementa:
            otra = por_id_todas.get(c)
            if otra is None:
                problemas.append(f"{r.id}: complementa a {c}, que no existe")
            elif c == r.id:
                problemas.append(f"{r.id}: se declara complementaria de si misma")
            elif r.vigente and not otra.vigente:
                problemas.append(
                    f"{r.id}: complementa a {c}, que esta DESCARTADA; una regla que no se ejecuta "
                    f"no refina nada"
                )

    fallbacks = [r.id for r in vigentes if r.clase == "fallback"]
    if len(fallbacks) > 1:
        problemas.append(
            f"hay {len(fallbacks)} reglas 'fallback' ({', '.join(fallbacks)}); la clausula else "
            f"es una, o no se sabe cual cierra"
        )

    # Mismo disparador EJECUTABLE y misma clase: o una declara que complementa a la otra, o cual
    # gana lo decide el orden del fichero, que es justo lo que ADR-0018 prohibe.
    import json as _json_pr

    por_disparo: dict[tuple[str, str], list[Regla]] = {}
    for r in vigentes:
        if not isinstance(r.forma, dict) or "cuando" not in r.forma:
            continue
        clave = (r.clase, _json_pr.dumps(r.forma["cuando"], sort_keys=True, ensure_ascii=False))
        por_disparo.setdefault(clave, []).append(r)
    for (clase, _cuando), grupo in sorted(por_disparo.items(), key=lambda x: x[0][0]):
        if len(grupo) < 2:
            continue
        ids = sorted(x.id for x in grupo)
        declarados = {c for x in grupo for c in (x.complementa or ())}
        if not any(x.id in declarados for x in grupo):
            problemas.append(
                f"{' y '.join(ids)}: misma clase '{clase}' y el MISMO disparador ejecutable, sin "
                f"que ninguna declare `complementa`; cual gana lo decidiria el orden del fichero"
            )

    # Dos reglas de la misma clase que actuan sobre el mismo parametro-disparador y declaran la
    # misma accion: sin precondicion que las separe, cual gana lo decidiria el orden del fichero.
    por_firma: dict[tuple[str, str], list[str]] = {}
    for r in vigentes:
        if not r.parametros:
            continue
        firma = (r.clase, " ".join(sorted(r.parametros)))
        por_firma.setdefault(firma, []).append(r.id)
    for (clase, params), rids in sorted(por_firma.items()):
        if len(rids) > 1:
            problemas.append(
                f"{', '.join(sorted(rids))}: misma clase ('{clase}') y exactamente los mismos "
                f"parametros ({params}); nada dice cual manda salvo el orden del fichero, que es "
                f"editorial. Dale a una de las dos la precondicion que la distingue"
            )

    # Y el solapamiento por subconjunto, que es como se tocan de verdad las reglas hermanas.
    conjuntos = {r.id: (r.clase, frozenset(r.parametros)) for r in vigentes if r.parametros}
    for a, (clase_a, pa) in sorted(conjuntos.items()):
        for b, (clase_b, pb) in sorted(conjuntos.items()):
            if a >= b or clase_a != clase_b or pa == pb:
                continue
            if pa < pb or pb < pa:
                menor, mayor = (a, b) if pa < pb else (b, a)
                por_id = {r.id: r for r in vigentes}
                if mayor in por_id[menor].complementa or menor in por_id[mayor].complementa:
                    continue  # se solapan A PROPOSITO y esta declarado
                problemas.append(
                    f"{menor} y {mayor}: misma clase ('{clase_a}') y los parametros de {menor} son "
                    f"un subconjunto de los de {mayor}; se solapan y nada dice cual manda. Si es "
                    f"a proposito -un invariante, o el mismo efecto para otro caso- declaralo con "
                    f"`complementa: [{mayor}]`"
                )
    return problemas


def cargar_vocabulario(ruta: Path) -> dict[str, dict[str, Any]]:
    """Predicados, hechos y acumuladores: el vocabulario con el que se escribe una regla.

    Viven en el MISMO fichero que las reglas y no en uno aparte. Un cuarto fichero rompia el
    contrato del hash por las dos vias -`cargar_manifiesto` exige `len(cubre) == 3`, ADR-0013 §5
    dice "los TRES ficheros" y MASTER_PLAN H.2 lo repite-, asi que habria obligado a enmendar los
    dos documentos a cambio de que alguien pudiera hashear tres de cuatro (ADR-0019).
    """
    try:
        doc = leer_yaml(ruta)
    except (OSError, YamlError) as exc:
        raise SpecError(f"{ruta.name}: {exc}") from exc
    if not isinstance(doc, dict):
        raise SpecError(f"{ruta.name}: no es un mapa")
    salida: dict[str, dict[str, Any]] = {}
    for seccion in ("predicados", "acciones", "efectos", "hechos", "acumuladores", "tokens"):
        bruto = doc.get(seccion) or {}
        if not isinstance(bruto, dict):
            raise SpecError(f"{ruta.name}: '{seccion}' debe ser un mapa")
        salida[seccion] = bruto
    return salida


def _invocaciones(nodo: Any) -> list[tuple[str, dict[str, Any]]]:
    """Todas las llamadas a predicado que hay en un arbol `cuando`/`entonces`."""
    fuera: list[tuple[str, dict[str, Any]]] = []
    if isinstance(nodo, list):
        for x in nodo:
            fuera += _invocaciones(x)
    elif isinstance(nodo, dict):
        for clave, valor in nodo.items():
            if clave == "pendiente_definicion":
                continue
            if clave in ("todos_de", "cualquiera_de", "ninguno_de", "cuando", "entonces", "hace"):
                fuera += _invocaciones(valor)
            elif clave in ("permite", "prohibe"):
                continue  # los mira `_efectos_invocados`: su contenido son nombres, no llamadas
            elif clave in _ESTRUCTURALES:
                continue  # `hecho`, `liga`, `distinta_de`...: son campos del nodo, no llamadas
            else:
                # Cualquier otra clave es una invocacion, LLEVE O NO un mapa de argumentos. Se
                # exigia `isinstance(valor, dict)`, asi que `{predicado_que_no_existe: "loquesea"}`
                # pasaba entero, sin vocabulario y sin argumentos que comprobar (F12, auditoria).
                #
                # Y la carga escalar NO se tira (F13, auditoria de cierre): se devolvia `{}`, o sea
                # que `en_ventana: "07:00 a 15:00 hora de Madrid, lunes a viernes"` colaba la
                # ventana entera como una frase en castellano dentro de la forma ejecutable y la
                # guardia daba OK. Viaja bajo la clave vacia, que ninguna regla puede escribir.
                if isinstance(valor, dict):
                    fuera.append((str(clave), valor))
                else:
                    fuera.append((str(clave), {"": valor}))
    return fuera


def _efectos_invocados(nodo: Any) -> list[str]:
    """Lo que una regla PERMITE o PROHIBE. No son acciones: son capacidades con nombre.

    No se comprobaban contra nada -`_invocaciones` los descartaba porque su valor es una lista-,
    asi que un `abrir_operacionn` con una ene de mas pasaba en once de las veinticuatro reglas
    vigentes (F12, auditoria de cierre).
    """
    fuera: list[str] = []
    if isinstance(nodo, list):
        for x in nodo:
            fuera += _efectos_invocados(x)
    elif isinstance(nodo, dict):
        for clave, valor in nodo.items():
            if clave in ("permite", "prohibe"):
                fuera += [str(v) for v in valor] if isinstance(valor, list) else [str(valor)]
            else:
                fuera += _efectos_invocados(valor)
    return fuera


# Argumentos que NO nombran un parametro: ligaduras, referencias y sujetos de geometria.
_ESTRUCTURALES = frozenset(
    {
        "liga",
        "distinta_de",
        "posterior_a",
        "que",
        "contra",
        "a",
        "de",
        "acumulador",
        "cual",
        "por",
        "resultado",
        "hecho",
        "a_la_baja",
    }
)
# NO hay lista de "argumentos de valor". Hasta F13 la habia -veinticinco nombres escritos a
# mano- y era una lista blanca al reves: solo se comprobaban los argumentos que figuraran en
# ella, asi que INVENTAR UN NOMBRE NUEVO bastaba para colar un valor de negocio crudo. Medido el
# 2026-09-12 sobre la spec real: `sentido` no estaba en la lista, y `sentido: alcista` pasaba sin
# una sola queja -que es exactamente el fallo que hundio la D1 original, el `cuerpo` horneado en
# el nombre de un predicado (ADR-0002), entrando por la otra puerta-.
#
# Ahora se niega por defecto: todo argumento de texto que no sea estructural lleva el NOMBRE de un
# parametro del registro o una LIGADURA del propio arbol. Anadir un argumento nuevo ya no es
# gratis; o nombra un parametro, o hay que declararlo estructural aqui, a la vista.
#
# Lo que esto TODAVIA no cubre, y queda declarado: el valor de un argumento estructural no se
# contrasta contra ningun catalogo -`que: liquidez_m15` y `que: cuerpo` son iguales para la
# guardia- porque los sujetos de geometria no estan declarados en ninguna parte. El glosario
# nombra "liquidez de M15" en prosa, no `liquidez_m15`, y cruzarlos seria inventar un contrato.


_ES_LIGADURA = re.compile(r"[A-Z][A-Z0-9_]{0,7}", re.ASCII)


def _ligaduras(nodo: Any) -> set[str]:
    """Variables que el propio arbol ata con `liga:` (`hecho: sesgo, liga: S` -> {"S"}).

    Una ligadura no es un valor de negocio ni un parametro: es un nombre que la regla se pone a
    si misma y que otro nodo del mismo arbol usa (`sentido: S`). Sin esto, negar por defecto
    denunciaria RN-005, que es correcta.
    """
    atadas: set[str] = set()
    if isinstance(nodo, dict):
        for clave, valor in nodo.items():
            # Con FORMA, o el agujero se reabre con una linea: `liga: alcista` bastaba para que
            # `sentido: alcista` volviera a pasar, que es justo el caso que esto existe para
            # impedir (F13, auditoria de cierre). Una ligadura es un nombre corto en mayusculas.
            if clave == "liga" and isinstance(valor, str) and _ES_LIGADURA.fullmatch(valor):
                atadas.add(valor)
            else:
                atadas |= _ligaduras(valor)
    elif isinstance(nodo, list):
        for hijo in nodo:
            atadas |= _ligaduras(hijo)
    return atadas


def _atadas_por_todos_de(nodo: Any, por_todos_de: bool = True) -> set[str]:
    """Las ligaduras que el `cuando` ata en un camino de `todos_de` desde la raiz.

    `_ligaduras` recoge TODO `liga:` del arbol, y eso sirve para negar por defecto -que el nombre
    exista- pero no para saber si la ligadura tiene VALOR cuando se usa. Una atada dentro de una
    rama de `cualquiera_de` solo vale si esa rama fue la que se cumplio, y dentro de `ninguno_de`
    no vale nunca: ADR-0019 no da semantica a ninguna de las dos. RN-029 llevo hasta el 2026-09-14
    un `cerrar_a_mercado: {de: OP}` con OP sin atar, y lo cazo el consultor a mano: OP es tambien
    un token declarado, asi que la guardia de argumentos lo daba por bueno.
    """
    atadas: set[str] = set()
    if isinstance(nodo, list):
        for hijo in nodo:
            atadas |= _atadas_por_todos_de(hijo, por_todos_de)
    elif isinstance(nodo, dict):
        liga = nodo.get("liga")
        if por_todos_de and isinstance(liga, str) and _ES_LIGADURA.fullmatch(liga):
            atadas.add(liga)
        for clave, valor in nodo.items():
            if clave == "todos_de":
                atadas |= _atadas_por_todos_de(valor, por_todos_de)
            elif clave in ("cualquiera_de", "ninguno_de"):
                atadas |= _atadas_por_todos_de(valor, False)
            elif clave not in _ESTRUCTURALES and isinstance(valor, dict):
                # una invocacion: su `liga` va dentro del mapa de argumentos
                liga_inv = valor.get("liga")
                if por_todos_de and isinstance(liga_inv, str) and _ES_LIGADURA.fullmatch(liga_inv):
                    atadas.add(liga_inv)
    return atadas


def comprobar_ligaduras(regla: Regla) -> list[str]:
    """Toda ligadura que se USA esta atada en un `todos_de` del `cuando` de la misma regla.

    Mira la CLASE del nombre -la forma de una ligadura, mayusculas cortas- y no su nombre: `OP` es
    tambien un token declarado, y por eso el `de: OP` sin atar de RN-029 paso todas las guardias.
    Vale para `entonces` y para el propio `cuando` (RN-014 usa `OP.zona_de_entrada` dentro de el).
    """
    if not isinstance(regla.forma, dict):
        return []
    atadas = _atadas_por_todos_de(regla.forma.get("cuando"))
    problemas: list[str] = []
    for rama in ("cuando", "entonces"):
        for nombre, args in _invocaciones(regla.forma.get(rama)):
            for clave, valor in args.items():
                if clave == "liga" or not isinstance(valor, str):
                    continue
                cabeza = valor.split(".")[0]
                if _ES_LIGADURA.fullmatch(cabeza) and cabeza not in atadas:
                    problemas.append(
                        f"{regla.id}: '{nombre}.{clave}' usa la ligadura {cabeza}, que el `cuando` "
                        f"no ata en un `todos_de`; atada en una rama de `cualquiera_de` o de "
                        f"`ninguno_de` no tiene valor (ADR-0019)"
                    )
    return problemas


def parametros_leidos_por_las_formas(
    reglas: list[Regla],
    parametros: set[str],
    vocabulario: Mapping[str, Mapping[str, Any]] | None = None,
) -> set[str]:
    """Los parametros que alguna forma VIGENTE lee de verdad, directamente o por un acumulador."""
    leidos: set[str] = set()
    acumuladores_usados: set[str] = set()
    for r in reglas:
        if not r.vigente or not isinstance(r.forma, dict):
            continue
        for _nombre, args in _invocaciones(r.forma):
            for clave, valor in args.items():
                if not isinstance(valor, str):
                    continue
                if clave == "acumulador":
                    acumuladores_usados.add(valor)
                    continue
                raiz = valor.split(".")[-1]
                if raiz in parametros:
                    leidos.add(raiz)
    acumuladores = (vocabulario or {}).get("acumuladores") or {}
    for nombre in acumuladores_usados:
        datos = acumuladores.get(nombre)
        if not isinstance(datos, dict):
            continue
        for campo in ("base", "reinicia_con", "magnitud", "arrastra"):
            valor = datos.get(campo)
            if isinstance(valor, str) and valor in parametros:
                leidos.add(valor)
    return leidos


def comprobar_consumo(
    reglas: list[Regla],
    consumidores: Mapping[str, tuple[str, ...] | None],
    ids_validos: Mapping[str, str],
    con_valor: set[str] | None = None,
    vocabulario: Mapping[str, Mapping[str, Any]] | None = None,
) -> list[str]:
    """Todo parametro CON VALOR tiene un lector, y el lector existe.

    Un valor que ninguna regla nombra y que nadie declara leer es un valor que nadie vigila: se
    queda viejo sin que ninguna guardia lo note, porque las guardias miran las reglas. F11 dejo
    nueve asi -la ficha del instrumento, el reloj del broker, las cuentas, el modelo de llenado-,
    y no se arregla inventandoles una regla: eso seria hacer pasar por operativa del trader lo que
    decide el plan (ADR-0016). Se arregla declarando quien los lee: una regla vigente que los
    nombre, o la funcionalidad posterior que los consumira. Lo que se comprueba es que esa
    funcionalidad EXISTA en el plan, no que su fila de H.2 prometa consumirla: eso lo sostiene
    la revision humana, y conviene no creer que lo hace la maquina.

    `consumidores` es nombre -> `consumido_por` del registro, de TODOS los parametros: los ids se
    validan siempre, tambien en los que no tienen valor, que si no se quedaban sin comprobar.
    `con_valor` son los que ademas exigen tener un lector. `ids_validos` es id -> que es ("regla
    vigente", "regla", "funcionalidad", "ADR").

    LECTOR ES UNA FORMA, no una lista (2026-09-16). Hasta entonces bastaba con que el parametro
    figurara en la lista `parametros` de una regla vigente, y `firma_magnitud_vigilada` -que la
    firma vigila EQUITY, el hecho mas consecuente del reglamento- estaba en la lista de RN-029 y
    RN-030 sin que ninguna forma lo leyera: vivia solo en prosa. Ahora cuenta como leido si una
    forma vigente lo pasa como argumento, o si es un campo (`base`, `reinicia_con`, `magnitud`,
    `arrastra`) de un acumulador que una forma vigente usa.
    """
    problemas: list[str] = []
    nombrados = parametros_leidos_por_las_formas(reglas, set(consumidores), vocabulario)
    for nombre, declarados in sorted(consumidores.items()):
        # Los ids se validan SIEMPRE, tambien si una regla ya lo nombra: de lo contrario un
        # `consumido_por: [F99, RN-777]` colaba entero en cuanto cualquier regla mencionara el
        # parametro (F12, auditoria de cierre).
        for c in declarados or ():
            que_es = ids_validos.get(c)
            if que_es is None:
                problemas.append(f"{nombre}: declara `consumido_por: {c}`, que no existe")
            elif que_es == "regla":
                problemas.append(
                    f"{nombre}: declara `consumido_por: {c}`, que es una regla DESCARTADA; una "
                    f"regla que no esta vigente no lee nada"
                )
        if nombre in nombrados or (con_valor is not None and nombre not in con_valor):
            continue
        if not declarados:
            problemas.append(
                f"{nombre}: tiene valor y NINGUNA forma vigente lo lee; declara "
                f"`consumido_por` con la regla, la funcionalidad (MASTER_PLAN H.2) o el ADR "
                f"que lo lee"
            )
            continue
        for c in declarados:
            if ids_validos.get(c) == "regla vigente":
                # Declarar una regla que no lo nombra es peor que no declarar nada: pone un id
                # donde deberia haber un hueco, y la guardia de arriba ya no vuelve a mirar.
                problemas.append(
                    f"{nombre}: declara `consumido_por: {c}`, que es una regla vigente y NO lo "
                    f"nombra; o la regla lo nombra, o el consumidor es otro"
                )
    return problemas


def comprobar_citas_revocadas(
    reglas: list[Regla],
    terminos: list[Termino],
    vocabulario: Mapping[str, Mapping[str, Any]],
    revocados: Mapping[str, str],
) -> list[str]:
    """Nadie cita un registro de feedback que otro registro ya corrigio.

    Es la guardia que mas veces ha nacido corta. Nacio en F11 mirando solo `parametros.yaml`
    -P13: `cartuchos_reinicio` cito durante toda la funcionalidad un registro revocado por llevar
    una parafrasis del consultor en el campo del literal-. Se amplio a reglas y glosario cuando
    RN-013 acabo citando uno en el commit que arreglaba lo anterior. Y el 2026-09-11 se vio que el
    vocabulario que estreno F12 -predicados y acciones, que tambien llevan `cita` propia- seguia
    fuera: al cerrar el acuerdo del lotaje, `no_es_multiplo_de` se quedo citando el registro que
    ese mismo acuerdo acababa de revocar, y nada lo dijo.

    `revocados` es id revocado -> id que lo supersede.
    """
    citados: list[tuple[str, str]] = [(r.id, r.cita) for r in reglas]
    citados += [(f"glosario {x.termino!r}", x.cita) for x in terminos]
    for seccion in ("predicados", "acciones", "hechos", "acumuladores"):
        for nombre, datos in sorted((vocabulario.get(seccion) or {}).items()):
            if isinstance(datos, dict) and datos.get("cita"):
                citados.append((f"{seccion} {nombre!r}", str(datos["cita"])))
    return [
        f"{doc_id}: cita {cita_id}, que esta revocado por {revocados[cita_id]}"
        for doc_id, cita_id in citados
        if cita_id in revocados
    ]


def _hechos_nombrados(nodo: object) -> list[str]:
    """Los hechos que una rama de la forma nombra, por token exacto.

    Se hacia con `nombre in json.dumps(rama)`, y una subcadena bastaba: `sesgo` casaba dentro de
    `sesgo_h4_criterio_ruptura`, asi que `hechos.sesgo` podia declarar que RN-003 lo consume -no
    lo consume, lo produce- y la guardia lo bendecia. Peor: corregir la declaracion la hacia
    fallar, o sea que obligaba a mantener la mentira.
    """
    fuera: list[str] = []
    if isinstance(nodo, dict):
        for clave, valor in nodo.items():
            if clave == "hecho" and isinstance(valor, str):
                fuera.append(valor)
            else:
                fuera += _hechos_nombrados(valor)
    elif isinstance(nodo, list):
        for v in nodo:
            fuera += _hechos_nombrados(v)
    return fuera


def _problemas_de_argumento(
    rid: str,
    invocacion: str,
    clave: str,
    valor: Any,
    parametros: set[str],
    atadas: set[str],
    vocabulario: dict[str, dict[str, Any]],
) -> list[str]:
    """Un argumento lleva un NOMBRE: de parametro, de token declarado, de hecho, de acumulador o
    una ligadura del arbol. Nunca un valor de negocio.

    Antes de la auditoria de cierre de F13 esto tenia dos agujeros por los que cabia un valor
    crudo, los dos medidos sobre la spec real:
      - **el tipo**: se saltaba todo lo que no fuera texto, asi que cambiar `tope:
        perdida_maxima_diaria` por `tope: 9.5` no producia una sola queja, y el tope de perdida
        diaria pasaba de 4,5 a 9,5 sin pisar el registro;
      - **la clave estructural**: `que`, `a`, `por`, `resultado` y `cual` no se miraban en
        absoluto, asi que `que: cuerpo` valia lo mismo que `que: liquidez_m15`. Por eso nace
        `tokens` en el vocabulario: ahora los sujetos de geometria y los estados estan declarados
        y se contrastan como todo lo demas.
    """
    if not isinstance(valor, str):
        # Un booleano tambien: `a: no` sin comillas es el FALSO de YAML 1.1 mientras que `a: si`
        # es la cadena 'si', y RN-013 llevaba las dos formas en la misma casilla.
        return [
            f"{rid}: '{invocacion}.{clave}' vale {valor!r} ({type(valor).__name__}); un argumento "
            f"lleva el NOMBRE de un parametro o de un token, no un valor"
        ]
    cabeza, _, cola = valor.partition(".")
    conocidos = (
        parametros
        | atadas
        | set(vocabulario.get("tokens") or {})
        | set(vocabulario.get("hechos") or {})
        | set(vocabulario.get("acumuladores") or {})
    )
    if cola:
        # Notacion punteada: `OP.precio_entrada`, `OP.stop_fraccion_caja`. Las DOS mitades tienen
        # que existir; antes solo se miraba la ultima, asi que `NO_LIGADA.stop_fraccion_caja`
        # pasaba con un sujeto inventado.
        malas = [x for x in (cabeza, cola) if x not in conocidos]
        if malas:
            return [
                f"{rid}: '{invocacion}.{clave}' vale {valor!r} y {malas} no esta declarado "
                f"(parametro, token, hecho, acumulador o ligadura)"
            ]
        return []
    if valor in conocidos:
        return []
    return [
        f"{rid}: '{invocacion}.{clave}' vale {valor!r}, que no es un parametro del registro, ni "
        f"un token declarado, ni una ligadura del arbol; un argumento lleva el NOMBRE, no el valor"
    ]


# Las claves que admite cada seccion del vocabulario. Cerradas desde el 2026-09-16 (ADR-0032): la
# carga solo exigia que cada seccion fuera un mapa, asi que un `origen` o un `valores` mal escritos
# se ignoraban en silencio, y con ellos la guardia que dependia de que estuvieran bien escritos.
CLAVES_VOCABULARIO: dict[str, frozenset[str]] = {
    "predicados": frozenset(
        {
            "descripcion",
            "argumentos",
            "cita",
            "literal",
            "notas",
            "depende_de",
            "fuente",
            "lo_provoca",
            "valores",
            "lado_de_ruido",
        }
    ),
    "acciones": frozenset({"descripcion", "argumentos", "efecto", "cita", "literal", "notas"}),
    "efectos": frozenset({"descripcion"}),
    "hechos": frozenset(
        {"descripcion", "origen", "decision", "lo_provoca", "produce", "consume", "valores"}
    ),
    "acumuladores": frozenset(
        {"descripcion", "base", "reinicia_con", "magnitud", "arrastra", "cita"}
    ),
    "tokens": frozenset({"descripcion", "clase"}),
}
ORIGENES_HECHO = ("regla", "broker")
# De donde sale lo que un predicado evalua (ADR-0032). `broker` y `bot` son los que una accion
# PROVOCA: un evento de esas fuentes sin accion que lo produzca es una regla inalcanzable, que es
# lo que era `se_coloca_orden_limite`.
FUENTES_PREDICADO = ("mercado", "reloj", "broker", "bot", "motor", "acumulador")
CLASES_TOKEN = ("reinicio", "duracion")
# Los dos valores del hecho `sesgo`. NO son tokens: si lo fueran, `sentido: alcista` pasaria la
# guardia de argumentos, que es la puerta que cerro la auditoria de F13. Solo se usan como claves de
# `lado_de_ruido`, y tienen que estar las dos, o un sentido quedaria sin lado de ruido.
SENTIDOS_SESGO = ("alcista", "bajista")


def _acciones_ejecutadas(reglas: list[Regla]) -> set[str]:
    return {
        nombre
        for r in reglas
        if r.vigente and isinstance(r.forma, dict)
        for nombre, _ in _invocaciones(r.forma.get("entonces"))
    }


def _problemas_lo_provoca(
    quien: str,
    datos: Mapping[str, Any],
    vocabulario: Mapping[str, Mapping[str, Any]],
    ejecutadas: set[str],
    exige_efecto: bool = True,
) -> list[str]:
    """`lo_provoca` no vacio, con acciones que existen y que alguna regla vigente ejecuta."""
    lista = datos.get("lo_provoca")
    if not isinstance(lista, list) or not lista:
        return [
            f"{quien}: no declara `lo_provoca`; sin la accion que lo hace verdadero, quien lo lee "
            f"puede ser inalcanzable y nada lo diria"
        ]
    problemas: list[str] = []
    acciones = vocabulario.get("acciones") or {}
    for accion in lista:
        if accion not in acciones:
            problemas.append(f"{quien}: lo provoca '{accion}', que no esta en `acciones`")
        elif accion not in ejecutadas:
            problemas.append(
                f"{quien}: lo provoca '{accion}', y NINGUNA regla vigente la ejecuta; quien lo lee "
                f"es inalcanzable"
            )
        elif exige_efecto and not (acciones.get(accion) or {}).get("efecto"):
            problemas.append(
                f"{quien}: lo provoca '{accion}', que no declara `efecto`; una accion que cambia "
                f"el broker tiene que poder frenarla un gate (ADR-0032)"
            )
    return problemas


def comprobar_vocabulario(
    reglas: list[Regla], vocabulario: Mapping[str, Mapping[str, Any]]
) -> list[str]:
    """Claves cerradas, fuentes de predicado, efectos de accion, clases de token y valores.

    Todo lo que ADR-0032 anade al vocabulario, comprobado contra las formas y no solo contra si
    mismo: un `valores` que nadie compara es una lista decorativa.
    """
    problemas: list[str] = []
    for seccion, claves in CLAVES_VOCABULARIO.items():
        for nombre, datos in sorted((vocabulario.get(seccion) or {}).items()):
            if not isinstance(datos, dict):
                problemas.append(f"{seccion} '{nombre}': no es un mapa")
                continue
            sobran = sorted(set(datos) - claves)
            if sobran:
                problemas.append(f"{seccion} '{nombre}': claves desconocidas {sobran}")

    ejecutadas = _acciones_ejecutadas(reglas)
    tokens_decl = vocabulario.get("tokens") or {}
    efectos = vocabulario.get("efectos") or {}

    for nombre, datos in sorted(tokens_decl.items()):
        clase = datos.get("clase") if isinstance(datos, dict) else None
        if clase is not None and clase not in CLASES_TOKEN:
            problemas.append(f"tokens '{nombre}': clase {clase!r} no esta en {CLASES_TOKEN}")

    for nombre, datos in sorted((vocabulario.get("acciones") or {}).items()):
        efecto = datos.get("efecto") if isinstance(datos, dict) else None
        if efecto is not None and efecto not in efectos:
            problemas.append(f"acciones '{nombre}': efecto '{efecto}', que no esta en `efectos`")

    predicados = vocabulario.get("predicados") or {}
    for nombre, datos in sorted(predicados.items()):
        if not isinstance(datos, dict):
            continue
        fuente = datos.get("fuente")
        if fuente not in FUENTES_PREDICADO:
            problemas.append(
                f"predicados '{nombre}': fuente {fuente!r} no esta en {FUENTES_PREDICADO}; "
                f"sin ella no se sabe quien produce lo que evalua"
            )
        elif fuente in ("broker", "bot"):
            problemas += _problemas_lo_provoca(
                f"predicados '{nombre}'",
                datos,
                vocabulario,
                ejecutadas,
                exige_efecto=fuente == "broker",
            )
        elif "lo_provoca" in datos:
            problemas.append(
                f"predicados '{nombre}': `lo_provoca` solo va en predicados de fuente broker o bot"
            )
        valores = datos.get("valores")
        if valores is not None:
            if not isinstance(valores, dict):
                problemas.append(
                    f"predicados '{nombre}': `valores` debe ser un mapa argumento -> lista"
                )
            else:
                for arg, lista in valores.items():
                    if arg not in (datos.get("argumentos") or []):
                        problemas.append(
                            f"predicados '{nombre}': `valores` de '{arg}', que no es un argumento"
                        )
                    for v in lista if isinstance(lista, list) else [lista]:
                        if v not in tokens_decl:
                            problemas.append(
                                f"predicados '{nombre}': `valores` de '{arg}' incluye {v!r}, que "
                                f"no es un token declarado"
                            )
        lados = datos.get("lado_de_ruido")
        if lados is not None:
            if not isinstance(lados, dict) or not lados:
                problemas.append(f"predicados '{nombre}': `lado_de_ruido` debe ser un mapa")
            else:
                if sorted(lados) != sorted(SENTIDOS_SESGO):
                    problemas.append(
                        f"predicados '{nombre}': `lado_de_ruido` tiene que nombrar exactamente "
                        f"{SENTIDOS_SESGO}, y nombra {sorted(lados)}"
                    )
                for lado in lados.values():
                    if lado not in tokens_decl:
                        problemas.append(
                            f"predicados '{nombre}': `lado_de_ruido` usa {lado!r}, que no es un "
                            f"token declarado"
                        )
                if len(set(lados.values())) != len(lados):
                    problemas.append(
                        f"predicados '{nombre}': `lado_de_ruido` da el mismo lado a los dos "
                        f"sentidos"
                    )

    # Y los valores contra lo que las formas pasan de verdad.
    for r in reglas:
        if not isinstance(r.forma, dict):
            continue
        for nombre, args in _invocaciones(r.forma.get("cuando")):
            valores = (predicados.get(nombre) or {}).get("valores")
            if not isinstance(valores, dict):
                continue
            for arg, lista in valores.items():
                if arg in args and isinstance(lista, list) and args[arg] not in lista:
                    problemas.append(
                        f"{r.id}: '{nombre}.{arg}' vale {args[arg]!r}, fuera de su conjunto "
                        f"cerrado {lista}"
                    )
    return problemas


def es_ejecutable(regla: Any) -> bool:
    """Tiene forma Y su condicion esta definida.

    Una regla con `pendiente_definicion` TIENE `forma` y no se puede ejecutar. Contarla entre las
    ejecutables hacia que `spec status` dijera "0 todavia en prosa" mientras `docs/spec/reglas.md`
    decia de RN-028 "No es ejecutable todavia". Vive aqui y no en cada sitio que cuenta porque ya
    se habia arreglado en uno solo, y `knowledge validate` y `spec status` acabaron diciendo
    cifras distintas de la misma spec (F13, auditoria de cierre).
    """
    forma = getattr(regla, "forma", None)
    return isinstance(forma, dict) and forma.get("pendiente_definicion") is None


def comprobar_forma(
    reglas: list[Regla],
    vocabulario: dict[str, dict[str, Any]],
    parametros: set[str],
    ambiguedades_abiertas: set[str] | None = None,
    tipos: Mapping[str, str] | None = None,
    ids_adr: set[str] | None = None,
) -> list[str]:
    """Que la forma ejecutable use vocabulario que existe y no esconda valores de negocio.

    Es lo que F12 aporta y la prosa no permitia: un `cuando` en español se puede leer de dos
    maneras y nadie lo nota; una invocacion a un predicado que no existe, o un argumento de valor
    que no es el nombre de un parametro, se ven a la primera y se nombran por su id.
    """
    problemas: list[str] = comprobar_vocabulario(reglas, vocabulario)
    hechos = vocabulario["hechos"]
    acumuladores = vocabulario["acumuladores"]
    ejecutadas = _acciones_ejecutadas(reglas)

    for r in reglas:
        if not isinstance(r.forma, dict):
            if r.vigente:
                problemas.append(
                    f"{r.id}: es VIGENTE y no tiene forma ejecutable; el motor no puede "
                    f"implementarla sin interpretar su prosa"
                )
            continue
        # Una regla puede estar VIGENTE -la prohibicion sigue en pie- y aun asi no ser ejecutable
        # porque el corpus no define su condicion. Se declara, no se tapa: RN-008 depende de que
        # es un breaker, y eso no esta en ningun sitio (A-21).
        pendiente = r.forma.get("pendiente_definicion")
        if pendiente is not None:
            # No basta el FORMATO: `A-999` pasaba, y ademas eximia a la regla de tener forma
            # ejecutable. Es el mismo defecto que `ambiguedad_id` tenia en el registro y que ya
            # se arreglo alli (F12, auditoria de cierre).
            if not re.fullmatch(r"A-\d+", str(pendiente), re.ASCII):
                problemas.append(f"{r.id}: pendiente_definicion {pendiente!r} no tiene formato A-N")
            elif ambiguedades_abiertas is not None and str(pendiente) not in ambiguedades_abiertas:
                problemas.append(
                    f"{r.id}: pendiente_definicion {pendiente}, que no es una ambiguedad ABIERTA; "
                    f"o la ambiguedad existe y sigue abierta, o la regla ya se puede ejecutar"
                )
        problemas += comprobar_ligaduras(r)
        # Lo que se permite o se prohibe, contra su catalogo.
        for efecto in _efectos_invocados(r.forma):
            if efecto not in vocabulario.get("efectos", {}):
                problemas.append(f"{r.id}: permite o prohibe '{efecto}', que no esta en `efectos`")
        # Un predicado se EVALUA y una accion se EJECUTA: cada rama tiene su vocabulario. Meterlos
        # en el mismo saco fue el hueco que la guardia encontro al escribir las veinte restantes.
        atadas = _ligaduras(r.forma)
        for rama, catalogo, etiqueta in (
            (r.forma.get("cuando"), vocabulario["predicados"], "predicados"),
            (r.forma.get("entonces"), vocabulario["acciones"], "acciones"),
        ):
            for nombre, args in _invocaciones(rama):
                if nombre == "hecho":
                    continue
                if "" in args:
                    problemas.append(
                        f"{r.id}: '{nombre}' lleva {args['']!r} en vez de un mapa de argumentos; "
                        f"asi no hay nada que comprobar y ahi cabe cualquier cosa"
                    )
                if nombre in catalogo:
                    declarados = set(catalogo[nombre].get("argumentos") or [])
                    sobran = sorted(set(args) - declarados - _ESTRUCTURALES - {""})
                    if sobran:
                        problemas.append(
                            f"{r.id}: llama a '{nombre}' con argumentos que no declara: {sobran}"
                        )
                    # Y los que FALTAN, que es la direccion que borra una cota: quitar `fin` de
                    # `en_ventana` dejaba la ventana operativa sin final y todo en verde (F13,
                    # auditoria de cierre). Un argumento que de verdad sobre se quita del
                    # vocabulario, que para eso lo declara.
                    faltan = sorted(declarados - set(args))
                    if faltan and "" not in args:
                        problemas.append(
                            f"{r.id}: llama a '{nombre}' sin los argumentos que declara: {faltan}"
                        )
                else:
                    problemas.append(f"{r.id}: invoca '{nombre}', que no esta en `{etiqueta}`")
                for clave, valor in args.items():
                    problemas += _problemas_de_argumento(
                        r.id, nombre, clave, valor, parametros, atadas, vocabulario
                    )

    # Lo que la forma USA tiene que estar DECLARADO en `parametros`. Si no, las guardias que leen
    # esa lista se vuelven ciegas justo donde importa: `comprobar_decisiones` no ve que la regla
    # opera sobre un parametro de entorno, y la comprobacion de UNKNOWN no ve que una regla
    # VIGENTE ejecuta un valor que sigue en revision. Paso con las cuatro del piloto: RN-014
    # ejecutaba `break_even_criterio_ruptura` -DEFAULT_AMBIGUOUS bajo A-13- sin declararlo.
    for r in reglas:
        if not isinstance(r.forma, dict):
            continue
        # Por el ARBOL, no por el JSON serializado. Buscar el nombre entrecomillado dentro del
        # volcado daba falsos positivos -una CLAVE que se llama como un parametro (`parciales`),
        # o una variable ligada- y un falso negativo que la propia spec ya usa: la notacion
        # punteada `OP.stop_fraccion_caja` no casaba (F12, auditoria de cierre).
        usados: set[str] = set()
        for _nombre_inv, args in _invocaciones(r.forma):
            for clave, valor in args.items():
                if clave in _ESTRUCTURALES or not isinstance(valor, str):
                    continue
                raiz = valor.split(".")[-1]
                if raiz in parametros:
                    usados.add(raiz)
        sin_declarar = sorted(usados - set(r.parametros))
        if sin_declarar:
            problemas.append(
                f"{r.id}: su forma usa {', '.join(sin_declarar)} y no lo declara en `parametros`; "
                f"las guardias que leen esa lista no lo verian"
            )

    # Un hecho que nadie consume es una regla que no sirve; uno que nadie produce, una inalcanzable.
    # Y NO basta con mirar la declaracion: hay que compararla con lo que las formas hacen de verdad.
    # Comprobando solo la declaracion, `operativa_detenida` decia "consume: [RN-001]" mientras
    # RN-001 no lo leia, asi que el tope del 4,5 % prohibia abrir en el tick del evento y nada
    # impedia abrir en el siguiente; y `operacion_abierta` decia producirse en RN-011 sin que nadie
    # lo produjera, dejando el cierre forzoso y el break even INALCANZABLES. Los tres pasaban.
    #
    # Dos correcciones de la auditoria de cierre de F12 (2026-09-11):
    #  - se miraban SOLO los hechos declarados, asi que `liquidez_tomada` (RN-004) y `estructura_m1`
    #    (RN-007) se fijaban sin estar declarados y sin que nadie los leyera. El primero es la
    #    precondicion de los dos esquemas de entrada: un motor que implementara `forma` habria
    #    entrado sin esperar a que la liquidez de M15 se tomara.
    #  - la comparacion casaba por SUBCADENA: `hechos.sesgo` declaraba `consume: [RN-003, RN-005]`
    #    y colaba porque el `cuando` de RN-003 contiene `sesgo_h4_criterio_ruptura`. La guardia
    #    obligaba a mantener la declaracion falsa. Ahora casa el token exacto.
    ids_regla = {r.id for r in reglas}
    hechos_usados: set[str] = set()
    reales: dict[str, dict[str, list[str]]] = {}
    for r in reglas:
        if not isinstance(r.forma, dict):
            continue
        for papel, rama in (("consume", "cuando"), ("produce", "entonces")):
            for nombre in _hechos_nombrados(r.forma.get(rama)):
                hechos_usados.add(nombre)
                reales.setdefault(nombre, {"produce": [], "consume": []})[papel].append(r.id)

    # Un predicado tambien consume: `se_da_esquema` no se evalua sin `liquidez_tomada`. Lo declara
    # con `depende_de` en vez de en su prosa, que es donde vivia y donde nadie podia comprobarlo.
    for nombre_pred, datos in sorted(vocabulario["predicados"].items()):
        if not isinstance(datos, dict):
            continue
        for nombre in datos.get("depende_de") or []:
            hechos_usados.add(str(nombre))
            reales.setdefault(str(nombre), {"produce": [], "consume": []})["consume"].append(
                f"predicado {nombre_pred}"
            )

    for nombre in sorted(hechos_usados - set(hechos)):
        problemas.append(
            f"hecho '{nombre}': las formas lo usan y no esta declarado en `hechos`; nadie puede "
            f"comprobar quien lo produce ni quien lo consume"
        )

    for nombre, h in sorted(hechos.items()):
        real_de = reales.get(nombre, {"produce": [], "consume": []})
        origen = h.get("origen", "regla")
        if origen not in ORIGENES_HECHO:
            problemas.append(f"hecho '{nombre}': origen {origen!r} no esta en {ORIGENES_HECHO}")
            continue
        papeles: tuple[str, ...] = ("produce", "consume")
        if origen == "broker":
            # ADR-0028 §5 y ADR-0032: lo lee el motor del broker. Ninguna forma lo fija, y lo que
            # sustituye a "tiene un productor real" es que la accion que lo provoca exista y la
            # ejecute alguna regla vigente; si no, sus consumidores quedan inalcanzables en
            # silencio.
            papeles = ("consume",)
            if h.get("produce"):
                problemas.append(
                    f"hecho '{nombre}': es de origen broker y declara `produce`; lo lee el motor "
                    f"del estado de ordenes y posiciones, no lo produce una regla (ADR-0028 §5)"
                )
            for rid in sorted(set(real_de["produce"])):
                problemas.append(
                    f"{rid}: fija '{nombre}', que se deriva del broker (ADR-0028 §5); una regla no "
                    f"puede fijarlo, o la copia se desincroniza del broker"
                )
            decision_h = h.get("decision")
            if not (isinstance(decision_h, str) and re.fullmatch(r"ADR-\d{4}", decision_h)):
                problemas.append(
                    f"hecho '{nombre}': es de origen broker y no declara `decision` con el ADR que "
                    f"lo deriva"
                )
            elif ids_adr is not None and decision_h not in ids_adr:
                problemas.append(f"hecho '{nombre}': decision {decision_h}, que no existe")
            problemas += _problemas_lo_provoca(f"hecho '{nombre}'", h, vocabulario, ejecutadas)
        elif "lo_provoca" in h or "decision" in h:
            problemas.append(
                f"hecho '{nombre}': `lo_provoca` y `decision` son de un hecho de origen broker; "
                f"este es de origen regla y lo dice `produce`"
            )
        for papel in papeles:
            declarado = sorted(h.get(papel) or [])
            for rid in declarado:
                if rid not in ids_regla and not rid.startswith("predicado "):
                    problemas.append(f"hecho '{nombre}': {papel} {rid}, que no existe")
            real = sorted(real_de[papel])
            if not real:
                motivo = (
                    "nadie lo establece y quien lo lee es inalcanzable"
                    if papel == "produce"
                    else "quien lo establece no frena nada"
                )
                problemas.append(f"hecho '{nombre}': NINGUNA regla lo {papel} de verdad; {motivo}")
            elif real != declarado:
                problemas.append(
                    f"hecho '{nombre}': declara {papel}={declarado} y en las formas es {real}"
                )

    # Con que se fija cada hecho. Sin esto, `permanente` podia acabar en `detenido_por_tope` -que
    # RN-020 y RN-029 reescriben en cada evento sin mirar su valor- y la guardia no decia nada.
    for r in reglas:
        if not isinstance(r.forma, dict):
            continue
        for nombre_inv, args in _invocaciones(r.forma.get("entonces")):
            if nombre_inv != "fijar":
                continue
            h = hechos.get(str(args.get("hecho")))
            valores_h = h.get("valores") if isinstance(h, dict) else None
            if isinstance(valores_h, list) and args.get("a") not in valores_h:
                problemas.append(
                    f"{r.id}: fija '{args.get('hecho')}' a {args.get('a')!r}, que no esta en sus "
                    f"`valores` {valores_h}"
                )

    tokens_decl = vocabulario.get("tokens") or {}
    for nombre, a in sorted(acumuladores.items()):
        if a.get("base") not in parametros:
            problemas.append(
                f"acumulador '{nombre}': 'base' vale {a.get('base')!r}, que no es un parametro"
            )
        # `reinicia_con` es un reloj o un evento: un token de clase `reinicio` o un parametro enum
        # que diga cual. Nunca un booleano: `perdida_total_firma` llevaba ahi
        # `firma_perdida_total_arrastra`, que dice si la BASE sigue al maximo, no cuando se
        # reinicia.
        reinicio = a.get("reinicia_con")
        token_r = tokens_decl.get(reinicio) if isinstance(reinicio, str) else None
        if isinstance(token_r, dict):
            if token_r.get("clase") != "reinicio":
                problemas.append(
                    f"acumulador '{nombre}': 'reinicia_con' vale el token {reinicio!r}, que no es "
                    f"de clase `reinicio`"
                )
        elif reinicio not in parametros:
            problemas.append(
                f"acumulador '{nombre}': 'reinicia_con' vale {reinicio!r}, que no es un parametro "
                f"ni un token de reinicio"
            )
        elif tipos is not None and tipos.get(str(reinicio)) != "enum":
            problemas.append(
                f"acumulador '{nombre}': 'reinicia_con' vale el parametro {reinicio!r}, de tipo "
                f"{tipos.get(str(reinicio))}; un reinicio es un reloj o un evento, no un "
                f"{tipos.get(str(reinicio))}"
            )
        for campo, tipo_exigido in (("magnitud", "enum"), ("arrastra", "booleano")):
            if campo not in a:
                continue
            valor = a.get(campo)
            if valor not in parametros:
                problemas.append(
                    f"acumulador '{nombre}': '{campo}' vale {valor!r}, que no es un parametro"
                )
            elif tipos is not None and tipos.get(str(valor)) != tipo_exigido:
                problemas.append(
                    f"acumulador '{nombre}': '{campo}' vale {valor!r}, que no es de tipo "
                    f"{tipo_exigido}"
                )
    return problemas
