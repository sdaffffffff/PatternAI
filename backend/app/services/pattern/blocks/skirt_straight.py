"""
Straight skirt block — front and back panels + waistband.
All measurements in cm. Origin (0,0) at top-left of each piece.
"""
from app.services.pattern.sizing import get_measurements, LENGTHS_CM


SEAM = 1.5
HEM = 3.0


def generate(parameters: dict) -> dict:
    size   = parameters.get("size", "M")
    fit    = parameters.get("fit", "fitted")
    length = parameters.get("length", "midi")
    closure = parameters.get("closure", "left_side")
    waistband_type = parameters.get("waistband", "zipper")

    m = get_measurements(size, fit)
    skirt_length = LENGTHS_CM.get(length, 70)

    half_hip   = m["hip"] / 4
    half_waist = m["waist"] / 4
    hip_drop   = 20

    front = _panel(half_waist, half_hip, hip_drop, skirt_length, side="front")
    back  = _panel(half_waist, half_hip, hip_drop, skirt_length, side="back")
    waistband = _waistband(m["waist"], waistband_type)

    pieces = [front, back, waistband]

    notes = []
    if closure == "left_side":
        notes.append(f"Cremallera oculta en costura lateral izquierda, desde cintura hasta {skirt_length * 0.35:.0f}cm")
    elif closure == "back":
        notes.append("Cremallera oculta en costura central de espalda")
    elif closure == "elastic":
        notes.append("Cintura elástica — no incluir cremallera")

    return {
        "pieces": pieces,
        "notes": notes,
        "total_fabric_cm": _estimate_fabric(skirt_length, m["hip"]),
    }


def _panel(half_waist: float, half_hip: float, hip_drop: float, length: float, side: str) -> dict:
    w_top = half_waist + SEAM * 2
    w_hip = half_hip + SEAM * 2
    h = length + SEAM + HEM

    dart_width = (half_hip - half_waist) / 2
    dart_length = 12.0

    points = [
        [0, 0],
        [w_top, 0],
        [w_hip, hip_drop],
        [w_hip, h],
        [0, h],
        [0, 0],
    ]

    dart = {
        "x": w_top / 2,
        "y_top": 0,
        "width": dart_width,
        "length": dart_length,
    }

    return {
        "name": f"Falda {'Delantera' if side == 'front' else 'Trasera'}",
        "width_cm": round(w_hip, 2),
        "height_cm": round(h, 2),
        "points": [[round(x, 2), round(y, 2)] for x, y in points],
        "dart": dart if dart_width > 0.5 else None,
        "grain_line": {"x": w_hip / 2, "y_start": h * 0.1, "y_end": h * 0.9},
        "seam_allowance_cm": SEAM,
        "hem_allowance_cm": HEM,
    }


def _waistband(waist: float, waistband_type: str) -> dict:
    width  = waist + SEAM * 2 + (3 if waistband_type != "elastic" else 0)
    height = 4.0 + SEAM * 2

    return {
        "name": "Cinturilla",
        "width_cm": round(width, 2),
        "height_cm": round(height, 2),
        "points": [
            [0, 0], [width, 0], [width, height], [0, height], [0, 0]
        ],
        "grain_line": {"x": width / 2, "y_start": height * 0.1, "y_end": height * 0.9},
        "seam_allowance_cm": SEAM,
        "hem_allowance_cm": 0,
        "note": "Doblar por la mitad en horizontal — marcar línea de doblez",
    }


def _estimate_fabric(length: float, hip: float) -> dict:
    fabric_width = 150
    panels = 2
    waistband_height = 10
    total_height = (length + HEM + SEAM) * panels + waistband_height
    meters = total_height / 100

    return {
        "width_cm": fabric_width,
        "meters": round(meters + 0.2, 2),
        "note": "Estimación para tela de 150cm de ancho. Añadir 20cm extra si hay estampado con rapport.",
    }
