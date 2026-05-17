"""
Generates a DXF file compatible with industrial CAD systems (AAMA/ASTM standard).
Each pattern piece is placed on its own layer.
"""
from pathlib import Path
import ezdxf
from ezdxf.enums import TextEntityAlignment


def export(pattern: dict, output_path: Path) -> Path:
    doc = ezdxf.new(dxfversion="R2010")
    doc.header["$INSUNITS"] = 4  # cm

    msp = doc.modelspace()

    x_offset = 0.0
    gap = 5.0

    for piece in pattern["pieces"]:
        layer_name = piece["name"].replace(" ", "_").upper()
        doc.layers.add(name=layer_name)

        points = piece.get("points", [])
        if len(points) < 2:
            continue

        shifted = [(x + x_offset, y) for x, y in points]

        msp.add_lwpolyline(
            shifted,
            close=True,
            dxfattribs={"layer": layer_name, "lineweight": 50},
        )

        gl = piece.get("grain_line")
        if gl:
            msp.add_line(
                (gl["x"] + x_offset, gl["y_start"]),
                (gl["x"] + x_offset, gl["y_end"]),
                dxfattribs={"layer": layer_name, "color": 5},
            )

        dart = piece.get("dart")
        if dart:
            dx = dart["x"] + x_offset
            dy_top = dart["y_top"]
            dart_h = dart["length"]
            dart_w = dart["width"] / 2
            msp.add_line(
                (dx - dart_w, dy_top), (dx, dy_top + dart_h),
                dxfattribs={"layer": layer_name, "color": 1},
            )
            msp.add_line(
                (dx + dart_w, dy_top), (dx, dy_top + dart_h),
                dxfattribs={"layer": layer_name, "color": 1},
            )

        piece_width = piece.get("width_cm", 20)
        label_x = x_offset + piece_width / 2
        label_y = -3.0

        msp.add_text(
            piece["name"],
            dxfattribs={"layer": layer_name, "height": 1.0},
        ).set_placement((label_x, label_y), align=TextEntityAlignment.CENTER)

        params = pattern.get("parameters", {})
        size_label = params.get("size", "")
        msp.add_text(
            f"Talla {size_label} | SA {piece['seam_allowance_cm']}cm",
            dxfattribs={"layer": layer_name, "height": 0.6},
        ).set_placement((label_x, label_y - 1.5), align=TextEntityAlignment.CENTER)

        x_offset += piece_width + gap

    doc.saveas(str(output_path))
    return output_path
