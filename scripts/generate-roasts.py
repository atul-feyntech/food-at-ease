#!/usr/bin/env python3
"""
Mizan Roast Generator
Uses Gemini AI to generate witty, factual verdicts for food products.

Usage:
    python scripts/generate-roasts.py [--dry-run] [--product SLUG]

Environment:
    GEMINI_API_KEY - Required API key for Gemini

Options:
    --dry-run       Print prompts without making API calls
    --product SLUG  Only generate roast for specific product
    --force         Regenerate even if roast exists and is approved
"""

import json
import os
import sys
import argparse
import time
from pathlib import Path

try:
    import google.generativeai as genai
except ImportError:
    print("Error: google-generativeai package not installed.")
    print("Run: pip install google-generativeai")
    sys.exit(1)


SYSTEM_PROMPT = """You are Mizan, a brutally honest food analyst for Indian packaged foods.
Your job is to write short, witty verdicts ("roasts") that expose the truth about products.

Guidelines:
- Be factually accurate - base verdicts on actual nutrition data provided
- Use a mix of English and Hindi/Hinglish naturally
- Be witty but not mean-spirited
- Focus on health impact, not taste
- Mention specific concerning nutrients (sodium, sugar, etc.)
- Compare to daily limits when relevant
- Keep it short: 2-3 punchy sentences max
- Use memorable phrases like "sugar bomb", "sodium explosion", etc.
- Reference ICMR/FSSAI guidelines when appropriate

Tone examples:
- "Taste ka dhamaka, health ka tamasha."
- "Marketing mein 'healthy', reality mein not really."
- "Sodium itna ki BP bole 'hello ji'."

Output format: Return ONLY a JSON object with these fields:
{
    "title_en": "Short 3-4 word English title",
    "title_hi": "Same in Hindi/Hinglish",
    "verdict_en": "2-3 sentence English verdict",
    "verdict_hi": "Same in Hindi/Hinglish",
    "emoji": "Single relevant emoji"
}"""


def get_product_context(product: dict) -> str:
    """Generate context string for a product."""
    nutrients = product.get("nutrients", {})
    score = product.get("mizan_score", {})
    safe_limit = product.get("safe_limit", {})

    context = f"""
Product: {product['name']}
Brand: {product['brand']}
Category: {product['category']}
Package Size: {product.get('package_size_g', 'N/A')}g

MIZAN SCORE: {score.get('stars', 'N/A')} stars (Grade {score.get('grade', 'N/A')})
INR Score: {score.get('inr_score', 'N/A')} (lower is better)
Limiting Factors: {', '.join(score.get('limiting_factors', []))}

NUTRITION (per 100g):
- Energy: {nutrients.get('energy_kcal', 'N/A')} kcal
- Protein: {nutrients.get('protein_g', 'N/A')}g
- Total Fat: {nutrients.get('total_fat_g', 'N/A')}g
- Saturated Fat: {nutrients.get('saturated_fat_g', 'N/A')}g
- Carbohydrates: {nutrients.get('carbohydrates_g', 'N/A')}g
- Sugar: {nutrients.get('sugar_g', 'N/A')}g
- Sodium: {nutrients.get('sodium_mg', 'N/A')}mg
- Fiber: {nutrients.get('fiber_g', 'N/A')}g

SAFE LIMIT: {safe_limit.get('recommended_serving_g', 'N/A')}g per day
Limiting Factor: {safe_limit.get('limiting_factor', 'N/A')}
Daily % at safe limit:
- Sodium: {safe_limit.get('daily_percentages', {}).get('sodium', 'N/A')}%
- Sugar: {safe_limit.get('daily_percentages', {}).get('sugar', 'N/A')}%
- Sat Fat: {safe_limit.get('daily_percentages', {}).get('saturated_fat', 'N/A')}%

INGREDIENTS: {', '.join(product.get('ingredients', [])[:10])}...

KNOWN FLAGS: {', '.join(product.get('flags', []))}
"""
    return context


def generate_roast(product: dict, model, dry_run: bool = False) -> dict | None:
    """Generate a roast for a single product."""
    context = get_product_context(product)

    prompt = f"""Based on this product data, write a witty Mizan verdict:

{context}

Remember: Be factual, witty, and use Hinglish naturally. Output ONLY valid JSON."""

    if dry_run:
        print(f"\n--- DRY RUN for {product['name']} ---")
        print(prompt[:500] + "...")
        return None

    try:
        response = model.generate_content(
            [SYSTEM_PROMPT, prompt],
            generation_config={
                "temperature": 0.8,
                "top_p": 0.95,
                "max_output_tokens": 500,
            }
        )

        # Parse JSON from response
        text = response.text.strip()
        # Remove markdown code blocks if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        text = text.strip()

        roast_data = json.loads(text)

        # Add metadata
        roast_data["approved"] = False  # Requires human review
        roast_data["generated_at"] = time.strftime("%Y-%m-%d")

        return roast_data

    except json.JSONDecodeError as e:
        print(f"  Error parsing JSON for {product['name']}: {e}")
        print(f"  Raw response: {response.text[:200]}...")
        return None
    except Exception as e:
        print(f"  Error generating roast for {product['name']}: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Generate Mizan roasts using Gemini AI")
    parser.add_argument("--dry-run", action="store_true", help="Print prompts without API calls")
    parser.add_argument("--product", type=str, help="Only process specific product slug")
    parser.add_argument("--force", action="store_true", help="Regenerate even if approved")
    args = parser.parse_args()

    # Setup paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    products_file = project_root / "src" / "data" / "products.json"

    # Load products
    print(f"Loading products from: {products_file}")
    with open(products_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])
    print(f"Found {len(products)} products")

    # Initialize Gemini
    if not args.dry_run:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("Error: GEMINI_API_KEY environment variable not set")
            print("Set it with: export GEMINI_API_KEY='your-api-key'")
            sys.exit(1)

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        print("Gemini API initialized")
    else:
        model = None
        print("DRY RUN MODE - No API calls will be made")

    # Process products
    updated = 0
    skipped = 0

    for i, product in enumerate(products):
        slug = product.get("slug", "")

        # Filter by product if specified
        if args.product and slug != args.product:
            continue

        # Skip if already has approved roast (unless --force)
        existing_roast = product.get("roast", {})
        if existing_roast.get("approved") and not args.force:
            print(f"  Skipping {product['name']} (already approved)")
            skipped += 1
            continue

        print(f"\nProcessing: {product['name']} ({i+1}/{len(products)})")

        roast = generate_roast(product, model, args.dry_run)

        if roast:
            product["roast"] = roast
            updated += 1
            print(f"  Generated: {roast.get('title_en', 'N/A')}")

            # Rate limiting
            if not args.dry_run:
                time.sleep(1)  # Avoid hitting rate limits

    # Save results
    if not args.dry_run and updated > 0:
        data["products"] = products
        with open(products_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\nSaved {updated} updated roasts to {products_file}")

    print(f"\nSummary:")
    print(f"  Updated: {updated}")
    print(f"  Skipped: {skipped}")
    print(f"\nNOTE: All generated roasts have 'approved: false'")
    print("Review and set 'approved: true' before publishing.")


if __name__ == "__main__":
    main()
