import json
import anthropic
from app.core.config import settings

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

SYSTEM_PROMPT = """Eres el asistente de diseño de PatternAI. Tu trabajo es ayudar a diseñadores de moda a definir los detalles técnicos de su prenda para generar un patrón de costura.

REGLAS IMPORTANTES:
- Habla siempre en español
- Usa lenguaje de diseño, NUNCA terminología técnica de patronaje
- Haz UNA sola pregunta a la vez
- Las preguntas deben ser simples, con opciones claras cuando sea posible
- Cuando tengas suficiente información, devuelve los parámetros finales

FLUJO DE PREGUNTAS según tipo de prenda:

Para FALDA (skirt_straight, skirt_flared):
1. Largo: "¿Qué largo quieres para la falda? (mini / midi / maxi)"
2. Cierre: "¿Dónde va el cierre? (lateral izquierdo / espalda / sin cierre)"
3. Cintura: "¿Cómo quieres la cintura? (ajustada con goma / ajustada con cremallera / con cinturilla)"
4. Holgura: "¿Qué fit buscas? (muy ajustada / ajustada / cómoda / suelta)"
5. Talla: "¿Qué talla usamos de base? (XS / S / M / L / XL)"

Para TOP BÁSICO (top_basic):
1. Escote: "¿Cómo quieres el escote? (redondo / en V / cuadrado / barco)"
2. Largo: "¿Qué largo quieres? (crop hasta la cintura / normal hasta la cadera / largo)"
3. Holgura: "¿Qué fit buscas? (muy ajustado / ajustado / cómodo / oversized)"
4. Talla: "¿Qué talla usamos de base? (XS / S / M / L / XL)"

Cuando hayas recogido toda la información necesaria, responde con este JSON (y SOLO este JSON, sin texto antes ni después):
{
  "status": "complete",
  "parameters": {
    "garment_type": "...",
    "size": "XS|S|M|L|XL",
    "length": "mini|midi|maxi|crop|hip",
    "fit": "very_fitted|fitted|comfortable|loose",
    "closure": "left_side|back|front|none|elastic",
    "neckline": "round|v_neck|square|boat|null",
    "waistband": "elastic|zipper|waistband|null"
  }
}

Si aún necesitas más información, responde con:
{
  "status": "asking",
  "message": "tu pregunta aquí"
}"""


async def process_message(conversation: list, user_message: str, analysis: dict) -> dict:
    context = f"""El diseñador ha subido una imagen. El análisis detectó:
- Tipo de prenda: {analysis.get('garment_type')}
- Silueta: {analysis.get('detected_features', {}).get('silhouette')}
- Descripción: {analysis.get('design_language_description')}

Ahora debes hacer las preguntas necesarias para completar los parámetros del patrón."""

    messages = []
    if not conversation:
        messages.append({"role": "user", "content": context})
        messages.append({"role": "assistant", "content": json.dumps({"status": "asking", "message": "¡Me encanta tu diseño! Vamos a configurar el patrón. " + _first_question(analysis.get("garment_type", ""))})})

    for msg in conversation:
        messages.append(msg)

    messages.append({"role": "user", "content": user_message})

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=messages,
    )

    raw = response.content[0].text.strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {"status": "asking", "message": raw}

    conversation.append({"role": "user", "content": user_message})
    conversation.append({"role": "assistant", "content": raw})

    return result


def _first_question(garment_type: str) -> str:
    questions = {
        "skirt_straight": "¿Qué largo quieres para la falda? (mini / midi / maxi)",
        "skirt_flared": "¿Qué largo quieres para la falda? (mini / midi / maxi)",
        "top_basic": "¿Cómo quieres el escote? (redondo / en V / cuadrado / barco)",
        "blouse": "¿Cómo quieres el escote? (redondo / en V / cuadrado / barco)",
        "dress": "¿Qué largo quieres para el vestido? (mini / midi / maxi)",
    }
    return questions.get(garment_type, "¿Qué tipo de prenda quieres hacer?")


def get_opening_message(analysis: dict) -> dict:
    garment_type = analysis.get("garment_type", "")
    description = analysis.get("design_language_description", "")
    first_q = _first_question(garment_type)

    return {
        "status": "asking",
        "message": f"¡Me encanta tu diseño! {description} Vamos a configurar el patrón. {first_q}",
    }
