"""Salida determinista de las consultas (F08): tabla legible y JSON. Sin rutas absolutas, sin
hora, claves ordenadas. Los avisos NO van aqui (la CLI los manda a stderr)."""

from __future__ import annotations

import json
from collections.abc import Sequence

from botsito.corpus.transcripcion import formato_ms
from botsito.retrieval.consultas import TIPO_CONTRADICCION, TIPO_FOTOGRAMA, Resultado
from botsito.retrieval.indice import TIPO_SEGMENTO

CABECERA_TIEMPOS = "# tiempos de la cruda (la corregida no lleva tiempos propios; ADR-0007/0010)"
ANCHO_TEXTO = 100


def _marcas(r: Resultado) -> str:
    marcas: list[str] = []
    if r.tipo == TIPO_SEGMENTO:
        marcas += [f"<{s}>" for s in r.extra.get("senales") or []]
        if r.extra.get("duda_glosario"):
            marcas.append("<duda glosario>")
    if r.extra.get("reemplazado_por"):
        marcas.append(f"[superseded por {r.extra['reemplazado_por']}]")
    if r.extra.get("supersede"):
        marcas.append(f"[supersede {r.extra['supersede']}]")
    return " ".join(marcas)


def _recorta(texto: str, contexto: bool) -> str:
    plano = " ".join(texto.split())
    if contexto or len(plano) <= ANCHO_TEXTO:
        return plano
    return plano[: ANCHO_TEXTO - 1] + "…"


def tabla(resultados: Sequence[Resultado], contexto: bool = False) -> str:
    """Una linea por resultado: fuente, video, tiempos, tipo, fotograma, marcas, texto. Con
    `contexto`, lineas de continuacion indentadas (afirmacion/tema o corregida)."""
    lineas = [CABECERA_TIEMPOS]
    for r in resultados:
        foto = r.fotograma["referencia"] if r.fotograma else "-"
        if r.tipo == TIPO_FOTOGRAMA:
            ruta = r.fotograma["ruta"] if r.fotograma else None
            lineas.append(f"{r.fuente}\t{r.video}\t{formato_ms(r.t0_ms)}\t{r.tipo}\t{ruta or '-'}")
            continue
        if r.tipo == TIPO_CONTRADICCION:
            lineas.append(
                f"{r.fuente}\t{r.video}\t-\t{r.tipo}\t{', '.join(r.extra['items'])}\t{r.texto}"
            )
            continue
        lineas.append(
            f"{r.fuente}\t{r.video}\t{formato_ms(r.t0_ms)}-{formato_ms(r.t1_ms)}\t{r.tipo}\t{foto}\t"
            f"{_marcas(r)}\t{_recorta(r.texto, contexto)}"
        )
        if contexto:
            if r.tipo == TIPO_SEGMENTO and r.extra.get("texto_corregido"):
                lineas.append(
                    f"    [corregida] {' '.join(str(r.extra['texto_corregido']).split())}"
                )
            elif r.tipo != TIPO_SEGMENTO:
                lineas.append(
                    f"    afirmacion: {r.extra.get('afirmacion')} · tema: {r.extra.get('tema')}"
                    f" · valor: {r.extra.get('valor')} · {r.extra.get('tipo_item')} · "
                    f"{r.extra.get('confianza')}"
                )
            if r.fotograma and r.fotograma.get("ruta"):
                lineas.append(f"    fotograma: {r.fotograma['ruta']}")
    lineas.append(f"{len(resultados)} resultados")
    return "\n".join(lineas) + "\n"


def json_(resultados: Sequence[Resultado]) -> str:
    return (
        json.dumps(
            [r.como_dict() for r in resultados], ensure_ascii=False, sort_keys=True, indent=1
        )
        + "\n"
    )
