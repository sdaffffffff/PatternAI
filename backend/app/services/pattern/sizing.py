MEASUREMENTS = {
    "XS": {"bust": 80, "waist": 60, "hip": 86, "back_length": 38},
    "S":  {"bust": 84, "waist": 64, "hip": 90, "back_length": 39},
    "M":  {"bust": 88, "waist": 68, "hip": 94, "back_length": 40},
    "L":  {"bust": 96, "waist": 76, "hip": 102, "back_length": 41},
    "XL": {"bust": 104, "waist": 84, "hip": 110, "back_length": 42},
}

LENGTHS_CM = {
    "mini":  40,
    "midi":  70,
    "maxi":  100,
    "crop":  32,
    "hip":   55,
}

FIT_EASE = {
    "very_fitted":  {"bust": 2,  "waist": 2,  "hip": 2},
    "fitted":       {"bust": 4,  "waist": 4,  "hip": 4},
    "comfortable":  {"bust": 8,  "waist": 6,  "hip": 8},
    "loose":        {"bust": 14, "waist": 10, "hip": 14},
}


def get_measurements(size: str, fit: str) -> dict:
    base = MEASUREMENTS.get(size, MEASUREMENTS["M"])
    ease = FIT_EASE.get(fit, FIT_EASE["fitted"])
    return {
        "bust":        base["bust"]  + ease["bust"],
        "waist":       base["waist"] + ease["waist"],
        "hip":         base["hip"]   + ease["hip"],
        "back_length": base["back_length"],
    }
