#!/usr/bin/env python3
"""
Generate roasts using Gemini REST API (no SDK required).
"""

import json
import urllib.request
import urllib.error
import time
from pathlib import Path

API_KEY = "AIzaSyB_5Izc9B4qOfC7RcgYTu3PuhvwXGV2V00"

SYSTEM_PROMPT = """You are FoodAtEase, a brutally honest food analyst for Indian packaged foods.
Your job is to write short, witty verdicts ("roasts") that expose the truth about products.

Guidelines:
- Be factually accurate - base verdicts on actual nutrition data provided
- Use a mix of English and Hindi/Hinglish naturally
- Be witty but not mean-spirited
- Focus on health impact, not taste
- Keep it short: 2-3 punchy sentences max

Output format: Return ONLY a JSON object with these fields:
{
    "title_en": "Short 3-4 word English title",
    "title_hi": "Same in Hindi/Hinglish",
    "verdict_en": "2-3 sentence English verdict",
    "verdict_hi": "Same in Hindi/Hinglish",
    "emoji": "Single relevant emoji"
}"""

def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

    payload = {
        "contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\n\n{prompt}"}]}],
        "generationConfig": {"temperature": 0.8, "topP": 0.95, "maxOutputTokens": 500}
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            text = result['candidates'][0]['content']['parts'][0]['text']
            return text.strip()
    except Exception as e:
        print(f"API Error: {e}")
        return None

def generate_roast(product):
    nutrients = product.get('nutrients', {})
    score = product.get('mizan_score', {})

    prompt = f"""Generate a FoodAtEase verdict for this product:

Product: {product['name']}
Brand: {product['brand']}
FOODATEASE SCORE: {score.get('stars', 'N/A')} stars (Grade {score.get('grade', 'N/A')})

NUTRITION (per 100g):
- Energy: {nutrients.get('energy_kcal', 'N/A')} kcal
- Sugar: {nutrients.get('sugar_g', 'N/A')}g
- Sodium: {nutrients.get('sodium_mg', 'N/A')}mg
- Saturated Fat: {nutrients.get('saturated_fat_g', 'N/A')}g
- Protein: {nutrients.get('protein_g', 'N/A')}g

Limiting Factors: {', '.join(score.get('limiting_factors', []))}

Be factual, witty, use Hinglish naturally. Output ONLY valid JSON."""

    try:
        response = call_gemini(prompt)
        if not response:
            return None

        text = response
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        text = text.strip()

        roast = json.loads(text)
        roast["approved"] = False
        return roast
    except Exception as e:
        print(f"  Error: {e}")
        return None

def main():
    products_file = Path(__file__).parent.parent / "src" / "data" / "products.json"

    print(f"Loading: {products_file}")
    with open(products_file) as f:
        data = json.load(f)

    products = data.get('products', [])
    needs_roast = [p for p in products if not p.get('roast') or not (p['roast'].get('verdict_en') or p['roast'].get('text'))]

    print(f"Total products: {len(products)}")
    print(f"Need roasts: {len(needs_roast)}")

    if not needs_roast:
        print("All products have roasts!")
        return

    generated = 0
    batch_size = 20

    for i, product in enumerate(needs_roast):
        print(f"[{i+1}/{len(needs_roast)}] {product['name'][:40]}...", end=" ", flush=True)

        roast = generate_roast(product)
        if roast:
            product['roast'] = roast
            generated += 1
            print(f"✓ {roast.get('emoji', '')}")
        else:
            print("✗")

        # Save every batch
        if (i + 1) % batch_size == 0:
            print(f"\n💾 Saving progress ({generated} roasts)...")
            with open(products_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        time.sleep(0.3)  # Rate limiting - Gemini has generous limits

    # Final save
    print(f"\n💾 Saving final ({generated} roasts)...")
    with open(products_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Generated {generated} roasts")

if __name__ == "__main__":
    main()
