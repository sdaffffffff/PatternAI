"""
Basic sleeveless top block — front and back bodice.
All measurements in cm. Origin (0,0) at top-left of each piece.
"""
from app.services.pattern.sizing import get_measurements, LENGTHS_CM


SEAM = 1.5
HEM = 2.0

NECKLINE_DEPTH = {
    "round":  {"front": 8,  "back": 2},
    "v_neck": {"front": 18, "back": 2},
    "square": {"front": 10, "back": 2},
    "boat":   {"front": 4,  "back": 3},
}

NECKLINE_WIDTH = {
    "round":  8,
    "v_neck": 6,
    "square": 10,
    "boat":   14,
}


def generate(parameters: dict) -> dict:
    size    = parameters.get("size", "M")
    fit     = parameters.get("fit", "fitted")
    length  = parameters.get("length", "hip")
    neckline = parameters.get("neckline", "round")

    m = get_measurements(size, fit)
    top_length = LENGTHS_CM.get(length, 55)

    front = _bodice(m, top_length, neckline, side="front")
    back  = _bodice(m, top_length, neckline, side="back")

    return {
        "pieces": [front, back],
        "notes": [
            f"Escote {neckline.replace('_', ' ')} — aplicar vista o ribete de {SEAM * 2}cm",
            "Sisas: terminar con ribete o vista de sisa",
        ],
        "total_fabric_cm": _estimate_fabric(top_length, m["bust"]),
    }


def _bodice(m: dict, length: float, neckline: str, side: str) -> dict:
    half_bust  = m["bust"] / 4 + SEAM * 2
    half_waist = m["waist"] / 4 + SEAM * 2
    h = length + SEAM + HEM

    depth_key = "front" if side == "front" else "back"
    neck_depth = NECKLINE_DEPTH.get(neckline, NECKLINE_DEPTH["round"])[depth_key]
    neck_width = NECKLINE_WIDTH.get(neckline, 8)

    shoulder_width = half_bust * 0.6
    shoulder_slope = 2.5

    armhole_depth = m["bust"] / 4 * 0.35

    waist_suppression = (half_bust - half_waist) / 2

    points = [
        [neck_width / 2, 0],
        [shoulder_width, shoulder_slope],
        [half_bust, armhole_depth],
        [half_bust - waist_suppression * 0.5, h * 0.6],
        [half_bust, h],
        [0, h],
        [0, neck_depth],
        [neck_width / 2, 0],
    ]

    return {
        "name": f"Cuerpo {'Delantero' if side == 'front' else 'Trasero'}",
        "width_cm": round(half_bust, 2),
        "height_cm": round(h, 2),
        "points": [[round(x, 2), round(y, 2)] for x, y in points],
        "neckline": {
            "type": neckline,
            "depth_cm": neck_depth,
            "width_cm": neck_width,
        },
        "armhole_depth_cm": round(armhole_depth, 2),
        "grain_line": {"x": half_bust / 2, "y_start": h * 0.15, "y_end": h * 0.85},
        "seam_allowance_cm": SEAM,
        "hem_allowance_cm": HEM,
        "cut_on_fold": True,
        "fold_note": "Cortar en doblez — el borde izquierdo va al doblez de la tela",
    }


def _estimate_fabric(length: float, bust: float) -> dict:
    fabric_width = 150
    total_height = (length + HEM + SEAM) * 2
    meters = total_height / 100

    return {
        "width_cm": fabric_width,
        "meters": round(meters + 0.15, 2),
        "note": "Estimación para tela de 150cm de ancho.",
    }
