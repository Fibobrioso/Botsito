"""Hoja de revision de las propuestas de F07: un HTML estatico por script (reproducible), con la
CRUDA (no la corregida), el contexto del tramo y la ruta local del fotograma citado. No incrusta
PNG. Uso: `uv run python docs/validation/anexos/F07-evidence-extraction/hoja_revision.py`
desde la raiz del repo; escribe `revision.html` junto a este script."""

from __future__ import annotations

import html
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "src"))

from botsito.corpus.manifiestos_fotogramas import cargar_todos as cargar_fr  # noqa: E402
from botsito.corpus.manifiestos_fotogramas import carpeta_de  # noqa: E402
from botsito.evidence.propuestas import cargar_propuestas  # noqa: E402


def _fmt(ms: int) -> str:
    return f"{ms // 3600000}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d}"


def main() -> int:
    propuestas = cargar_propuestas(REPO / "knowledge" / "_proposals")
    frs = {f.id: f for f in cargar_fr(REPO)}
    datos = REPO / "data"
    partes: list[str] = [
        "<!doctype html><meta charset='utf-8'><title>Hoja de revision F07</title>",
        "<style>body{font:14px/1.4 system-ui;margin:24px;max-width:1100px}"
        "h2{margin-top:36px;border-top:2px solid #999;padding-top:12px}"
        ".item{border:1px solid #ccc;border-radius:6px;padding:10px 14px;margin:12px 0}"
        ".cita{background:#fff8dc;padding:6px 8px;border-left:4px solid #d4a017;margin:6px 0}"
        ".ctx{font-size:12px;color:#333;background:#f4f4f4;padding:6px 8px;max-height:220px;overflow:auto}"
        ".meta{color:#555;font-size:12px}.foto{font-family:monospace;font-size:12px}"
        "table{border-collapse:collapse}td,th{border:1px solid #ddd;padding:3px 6px;font-size:12px}"
        "</style>",
        "<h1>F07 · hoja de revision de propuestas de evidencia</h1>",
        "<p>Cada item se ha localizado por maquina en la CRUDA (la cita se copia tal cual, con los "
        "errores del reconocedor). Decide por item: <b>aceptar</b> (la afirmacion, el tema y el valor "
        "no dicen mas que la cita), <b>rechazar</b> (con motivo) o <b>fotograma visto</b> para los "
        "items de pantalla (abre la ruta local indicada). Responde por lotes: "
        "\"acepto todos salvo pr-... item n (motivo)\".</p>",
    ]
    total = 0
    for p in propuestas:
        pid = p["propuesta_id"]
        partes.append(
            f"<h2>{html.escape(pid)}</h2><p class='meta'>video {p['video_id']} · "
            f"{p['t0']}-{p['t1']} · cruda {html.escape(p['transcripcion'])} · modelo "
            f"{html.escape(p['modelo'])} · {len(p['items'])} items · "
            f"{len(p['no_consta'])} no_consta · sello {'si' if p.get('salida_sha256') else 'NO'}</p>"
        )
        segmentos = {s["n"]: s for s in p["contexto"]["segmentos"]}
        for it in p["items"]:
            total += 1
            t0s, t1s = it["t0"], it["t1"]
            partes.append(f"<div class='item'><b>item {it['n']}</b> · {t0s}-{t1s} · "
                          f"{it['modalidad']} · {it['tipo']} · <code>{html.escape(it['tema'])}</code>"
                          + (f" · valor <b>{html.escape(str(it['valor']))}</b>" if it.get("valor") else "")
                          + f" · confianza {it['confianza']}"
                          + (f" · marca heredada {html.escape(it['marca_heredada'])}" if it.get("marca_heredada") else "")
                          + (f" · <b>decision: {it['decision']}</b>" if it.get("decision") else ""))
            partes.append(f"<div class='cita'>{html.escape(it['cita_literal'])}</div>")
            partes.append(f"<div>Afirmacion: {html.escape(it['afirmacion'])}</div>")
            if it.get("notas"):
                partes.append(f"<div class='meta'>Notas: {html.escape(it['notas'])}</div>")
            for ref in it.get("fotogramas") or []:
                ruta = ""
                if "/" in ref and ref.startswith("fr-"):
                    fid, t_ms = ref.rsplit("/", 1)
                    if fid in frs:
                        ruta = str(carpeta_de(datos, frs[fid]) / f"{t_ms}.png")
                partes.append(f"<div class='foto'>fotograma {html.escape(ref)} → {html.escape(ruta)}</div>")
            # contexto: segmentos del tramo del item (± 1)
            from botsito.evidence.modelo import parse_tiempo

            a, b = int(parse_tiempo(t0s) * 1000) - 2000, int(parse_tiempo(t1s) * 1000) + 2000
            ctx = [s for s in segmentos.values() if s["t1_ms"] > a and s["t0_ms"] < b]
            partes.append("<div class='ctx'>" + "<br>".join(
                f"[{_fmt(s['t0_ms'])}] {html.escape(s['texto'])}"
                + (f" <i>&lt;{','.join(s['senales'])}&gt;</i>" if s.get("senales") else "")
                for s in ctx
            ) + "</div></div>")
        if p["no_consta"]:
            partes.append("<table><tr><th>no consta (tema)</th><th>motivo</th></tr>" + "".join(
                f"<tr><td>{html.escape(n['tema'])}</td><td>{html.escape(n['motivo'])}</td></tr>"
                for n in p["no_consta"]) + "</table>")
    partes.insert(4, f"<p><b>{len(propuestas)} propuestas · {total} items propuestos</b></p>")
    salida = Path(__file__).with_name("revision.html")
    salida.write_text("\n".join(partes), encoding="utf-8", newline="\n")
    print(f"OK: {salida} ({len(propuestas)} propuestas, {total} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
