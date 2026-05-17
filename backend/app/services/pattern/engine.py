from app.services.pattern.blocks import skirt_straight, top_basic

SUPPORTED_GARMENTS = {
    "skirt_straight": skirt_straight.generate,
    "skirt_flared":   skirt_straight.generate,
    "top_basic":      top_basic.generate,
}


def generate_pattern(parameters: dict) -> dict:
    garment_type = parameters.get("garment_type")
    generator = SUPPORTED_GARMENTS.get(garment_type)

    if not generator:
        raise ValueError(f"Garment type '{garment_type}' not supported in this version.")

    pattern = generator(parameters)
    pattern["garment_type"] = garment_type
    pattern["parameters"] = parameters
    return pattern
