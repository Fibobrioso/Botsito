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
        "hechos",
        "acumuladores",
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
    reglas: list[Regla], textos: dict[str, str], terminos: list[Termino] | None = None
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
            # correcto HOY. Se deja anotado porque el dia que algo con cita propia -un predicado,
            # F12- no pase por `comprobar_contra`, esta guardia se apagaria sin avisar.
            continue
        if not literal_coincide(r.literal, citado):
            problemas.append(
                f"{r.id}: su literal no aparece en {r.cita}; una regla no puede decir algo "
                f"distinto de lo que cita"
            )
    return problemas


def comprobar_contra(
    reglas: list[Regla],
    terminos: list[Termino],
    parametros: set[str],
    citas_conocidas: set[str],
) -> list[str]:
    """Que cada regla nombre parametros que existen y cite algo que existe."""
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

    LO QUE ESTA FUNCION NO HACE, y conviene no creer que hace: NO habria cazado ninguno de esos
    tres pares. Se comprobo ejecutandola sobre la spec anterior al arreglo y devolvio cero
    hallazgos, porque RN-006 y RN-014 no comparten ningun parametro y RN-019 y RN-020 tampoco.
    Decidir que dos reglas actuan "sobre el mismo evento" exige leer `cuando`, que hoy es prosa;
    esa comprobacion es el trabajo de F12 y NO existe todavia.

    Lo que si comprueba, que es poco pero es cierto: que haya exactamente un `fallback`; que dos
    reglas de la misma clase no tengan exactamente los mismos parametros (un clon); y que los
    parametros de una no sean un SUBCONJUNTO de los de otra de su clase, que es la forma en que
    RN-017 se solapa con RN-016 y RN-013 con RN-011.
    """
    problemas: list[str] = []
    vigentes = [r for r in reglas if r.vigente]

    fallbacks = [r.id for r in vigentes if r.clase == "fallback"]
    if len(fallbacks) > 1:
        problemas.append(
            f"hay {len(fallbacks)} reglas 'fallback' ({', '.join(fallbacks)}); la clausula else "
            f"es una, o no se sabe cual cierra"
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
    for seccion in ("predicados", "acciones", "hechos", "acumuladores"):
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
            elif isinstance(valor, dict):
                fuera.append((str(clave), valor))
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
# Y los que SI: su valor tiene que ser el nombre de un parametro del registro. Cualquier otra cosa
# seria un valor de negocio escondido en un campo ejecutable, que es el fallo que hundio la D1
# original -el `cuerpo` horneado en el nombre de un predicado-.
_ARGS_DE_VALOR = frozenset(
    {
        "tope",
        "cadencia",
        "hora",
        "huso",
        "inicio",
        "fin",
        "dias",
        "nivel",
        "donde",
        "segun",
        "si",
        "cuando",
        "multiplo",
        "sobre",
        "extension",
        "parciales",
        "riesgo",
        "base",
        "fraccion",
        "paso",
        "minimo",
        "contrato",
        "cuenta_como",
        "noticias",
        "spread",
        "stop",
    }
)


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
    for seccion in ("predicados", "acciones"):
        for nombre, datos in sorted((vocabulario.get(seccion) or {}).items()):
            if isinstance(datos, dict) and datos.get("cita"):
                citados.append((f"{seccion} {nombre!r}", str(datos["cita"])))
    return [
        f"{doc_id}: cita {cita_id}, que esta revocado por {revocados[cita_id]}"
        for doc_id, cita_id in citados
        if cita_id in revocados
    ]


def comprobar_forma(
    reglas: list[Regla], vocabulario: dict[str, dict[str, Any]], parametros: set[str]
) -> list[str]:
    """Que la forma ejecutable use vocabulario que existe y no esconda valores de negocio.

    Es lo que F12 aporta y la prosa no permitia: un `cuando` en español se puede leer de dos
    maneras y nadie lo nota; una invocacion a un predicado que no existe, o un argumento de valor
    que no es el nombre de un parametro, se ven a la primera y se nombran por su id.
    """
    problemas: list[str] = []
    hechos = vocabulario["hechos"]
    acumuladores = vocabulario["acumuladores"]

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
        if pendiente is not None and not re.fullmatch(r"A-\d+", str(pendiente), re.ASCII):
            problemas.append(f"{r.id}: pendiente_definicion {pendiente!r} no tiene formato A-N")
        # Un predicado se EVALUA y una accion se EJECUTA: cada rama tiene su vocabulario. Meterlos
        # en el mismo saco fue el hueco que la guardia encontro al escribir las veinte restantes.
        for rama, catalogo, etiqueta in (
            (r.forma.get("cuando"), vocabulario["predicados"], "predicados"),
            (r.forma.get("entonces"), vocabulario["acciones"], "acciones"),
        ):
            for nombre, args in _invocaciones(rama):
                if nombre == "hecho":
                    continue
                if nombre in catalogo:
                    declarados = set(catalogo[nombre].get("argumentos") or [])
                    sobran = sorted(set(args) - declarados - _ESTRUCTURALES)
                    if sobran:
                        problemas.append(
                            f"{r.id}: llama a '{nombre}' con argumentos que no declara: {sobran}"
                        )
                else:
                    problemas.append(f"{r.id}: invoca '{nombre}', que no esta en `{etiqueta}`")
                for clave, valor in args.items():
                    if clave in _ESTRUCTURALES or not isinstance(valor, str):
                        continue
                    if (clave in _ARGS_DE_VALOR or clave.endswith("criterio")) and (
                        valor not in parametros
                    ):
                        problemas.append(
                            f"{r.id}: '{nombre}.{clave}' vale {valor!r}, que no es un parametro "
                            f"del registro; un argumento de valor lleva el NOMBRE, no el valor"
                        )

    # Un hecho que nadie consume es una regla que no sirve; uno que nadie produce, una inalcanzable.
    # Y NO basta con mirar la declaracion: hay que compararla con lo que las formas hacen de verdad.
    # Comprobando solo la declaracion, `operativa_detenida` decia "consume: [RN-001]" mientras
    # RN-001 no lo leia, asi que el tope del 4,5 % prohibia abrir en el tick del evento y nada
    # impedia abrir en el siguiente; y `operacion_abierta` decia producirse en RN-011 sin que nadie
    # lo produjera, dejando el cierre forzoso y el break even INALCANZABLES. Los tres pasaban.
    import json as _json

    ids_regla = {r.id for r in reglas}
    reales: dict[str, dict[str, list[str]]] = {}
    for nombre in hechos:
        reales[nombre] = {"produce": [], "consume": []}
        for r in reglas:
            if not isinstance(r.forma, dict):
                continue
            for papel, rama in (("consume", "cuando"), ("produce", "entonces")):
                if nombre in _json.dumps(r.forma.get(rama, {}), ensure_ascii=False):
                    reales[nombre][papel].append(r.id)

    for nombre, h in sorted(hechos.items()):
        for papel in ("produce", "consume"):
            declarado = sorted(h.get(papel) or [])
            for rid in declarado:
                if rid not in ids_regla:
                    problemas.append(f"hecho '{nombre}': {papel} {rid}, que no existe")
            real = sorted(reales[nombre][papel])
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

    for nombre, a in sorted(acumuladores.items()):
        for campo in ("base", "reinicia_con"):
            valor = a.get(campo)
            if valor not in parametros:
                problemas.append(
                    f"acumulador '{nombre}': '{campo}' vale {valor!r}, que no es un parametro"
                )
    return problemas
