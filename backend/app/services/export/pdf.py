"""
Generates a PDF with pattern pieces at 1:5 scale (1cm on paper = 5cm real).
"""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors

SCALE = 0.2
PAGE_W, PAGE_H = A4
MARGIN = 1.5 * cm


def export(pattern: dict, output_path: Path) -> Path:
    c = canvas.Canvas(str(output_path), pagesize=A4)

    _draw_cover(c, pattern)

    for piece in pattern["pieces"]:
        c.showPage()
        _draw_piece(c, piece)

    c.showPage()
    _draw_notes(c, pattern)

    c.save()
    return output_path


def _draw_cover(c: canvas.Canvas, pattern: dict):
    c.setFont("Helvetica-Bold", 20)
    c.drawString(MARGIN, PAGE_H - 3 * cm, "PatternAI")

    c.setFont("Helvetica", 14)
    garment_names = {
        "skirt_straight": "Falda Recta",
        "skirt_flared":   "Falda Evasé",
        "top_basic":      "Top Básico",
    }
    garment_name = garment_names.get(pattern.get("garment_type", ""), pattern.get("garment_type", ""))
    c.drawString(MARGIN, PAGE_H - 4.5 * cm, f"Prenda: {garment_name}")

    params = pattern.get("parameters", {})
    c.setFont("Helvetica", 11)
    y = PAGE_H - 6 * cm
    for key, value in params.items():
        if key != "garment_type":
            label = key.replace("_", " ").capitalize()
            c.drawString(MARGIN, y, f"{label}: {value}")
            y -= 0.7 * cm

    fabric = pattern.get("total_fabric_cm", {})
    if fabric:
        y -= 0.5 * cm
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN, y, "Tela necesaria:")
        y -= 0.7 * cm
        c.setFont("Helvetica", 11)
        c.drawString(MARGIN, y, f"{fabric.get('meters', '?')} metros × {fabric.get('width_cm', 150)}cm de ancho")
        y -= 0.7 * cm
        c.drawString(MARGIN, y, fabric.get("note", ""))

    c.setFont("Helvetica", 9)
    c.setFillColor(colors.grey)
    c.drawString(MARGIN, 2 * cm, "Escala 1:5 — 1cm en papel = 5cm real. Incluye márgenes de costura indicados.")
    c.setFillColor(colors.black)


def _draw_piece(c: canvas.Canvas, piece: dict):
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, PAGE_H - 2 * cm, piece["name"])

    c.setFont("Helvetica", 9)
    c.drawString(MARGIN, PAGE_H - 2.8 * cm,
                 f"Margen costura: {piece['seam_allowance_cm']}cm | Dobladillo: {piece['hem_allowance_cm']}cm")

    offset_x = MARGIN
    offset_y = PAGE_H - 4 * cm

    points = piece["points"]
    if not points:
        return

    scaled = [(offset_x + x * SCALE * cm, offset_y - y * SCALE * cm) for x, y in points]

    p = c.beginPath()
    p.moveTo(*scaled[0])
    for pt in scaled[1:]:
        p.lineTo(*pt)
    p.close()

    c.setStrokeColor(colors.black)
    c.setLineWidth(1.5)
    c.drawPath(p)

    gl = piece.get("grain_line")
    if gl:
        gx = offset_x + gl["x"] * SCALE * cm
        gy_start = offset_y - gl["y_start"] * SCALE * cm
        gy_end   = offset_y - gl["y_end"]   * SCALE * cm
        c.setStrokeColor(colors.blue)
        c.setLineWidth(0.8)
        c.line(gx, gy_start, gx, gy_end)
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.blue)
        c.drawCentredString(gx, gy_end - 0.4 * cm, "↕ hilo")
        c.setFillColor(colors.black)

    dart = piece.get("dart")
    if dart:
        dx = offset_x + dart["x"] * SCALE * cm
        dy_top = offset_y - dart["y_top"] * SCALE * cm
        dart_h = dart["length"] * SCALE * cm
        dart_w = dart["width"] * SCALE * cm / 2
        c.setStrokeColor(colors.red)
        c.setLineWidth(0.8)
        c.line(dx - dart_w, dy_top, dx, dy_top - dart_h)
        c.line(dx + dart_w, dy_top, dx, dy_top - dart_h)

    if piece.get("cut_on_fold"):
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(colors.darkgreen)
        c.drawString(MARGIN, MARGIN + 0.5 * cm, piece.get("fold_note", "Cortar en doblez"))
        c.setFillColor(colors.black)


def _draw_notes(c: canvas.Canvas, pattern: dict):
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, PAGE_H - 2 * cm, "Notas de Confección")

    notes = pattern.get("notes", [])
    c.setFont("Helvetica", 11)
    y = PAGE_H - 3.5 * cm
    for note in notes:
        c.drawString(MARGIN, y, f"• {note}")
        y -= 0.8 * cm
