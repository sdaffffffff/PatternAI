import base64
from pathlib import Path
import anthropic
from app.core.config import settings

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

ANALYSIS_PROMPT = """Eres un experto en patronaje de moda. Analiza esta imagen de una prenda o sketch de moda.

Responde ÚNICAMENTE con un JSON con esta estructura exacta:
{
  "garment_type": "skirt_straight | skirt_flared | top_basic | blouse | dress",
  "confidence": 0.0-1.0,
  "detected_features": {
    "silhouette": "descripción de la silueta",
    "neckline": "tipo de escote o null si no aplica",
    "sleeves": "tipo de manga o null si no aplica",
    "closure": "lateral | back | front | none",
    "length": "mini | midi | maxi | crop",
    "volume": "fitted | semi-fitted | loose | oversized"
  },
  "design_language_description": "Descripción de la prenda en términos de diseño, máximo 2 frases"
}

Solo devuelve el JSON, sin texto adicional."""


async def analyze_image(image_path: Path) -> dict:
    image_data = base64.standard_b64encode(image_path.read_bytes()).decode("utf-8")

    suffix = image_path.suffix.lower()
    media_types = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
    media_type = media_types.get(suffix, "image/jpeg")

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_data}},
                    {"type": "text", "text": ANALYSIS_PROMPT},
                ],
            }
        ],
    )

    import json
    text = message.content[0].text.strip()
    return json.loads(text)
