import json
import re
from typing import List
from openai import OpenAI
from .config import settings
from .models import ShortIdea


def parse_amount(instruction: str) -> int:
    m = re.search(r"(\d+)", instruction)
    if not m:
        return 4
    return max(1, min(20, int(m.group(1))))


def generate_ideas(instruction: str) -> List[ShortIdea]:
    amount = parse_amount(instruction)
    client = OpenAI(api_key=settings.openai_api_key)

    prompt = f"""
Du bist Creative Director für YouTube Shorts im Bereich satisfying simulation/vfx.
Erzeuge GENAU {amount} Ideen als JSON-Array.
Jedes Objekt hat: title, hook, visual_prompt, description.
- title: max 70 Zeichen, mit '#shorts'
- visual_prompt: für Video-AI, 9:16, loopfähig, hohe visuelle Qualität
- description: 1-2 Sätze + Hashtags
Antworte NUR mit gültigem JSON.
"""
    res = client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
    )
    content = res.choices[0].message.content or "[]"
    data = json.loads(content)
    return [ShortIdea(**x) for x in data]
