#!/usr/bin/env python3
"""
Fetch ALL Indian products with nutrition data from Open Food Facts.
"""

import json
import urllib.request
import urllib.parse
import time
import re
from pathlib import Path
from collections import defaultdict

API_BASE = "https://world.openfoodfacts.org/api/v2/search"

CATEGORY_MAP = {
    "biscuit": "biscuits", "cookie": "biscuits", "wafer": "biscuits", "rusk": "biscuits",
    "chips": "namkeen", "snack": "namkeen", "namkeen": "namkeen", "crisp": "namkeen",
    "kurkure": "namkeen", "bhujia": "namkeen", "mixture": "namkeen", "papad": "namkeen",
    "juice": "drinks", "drink": "drinks", "soda": "drinks", "cola": "drinks",
    "beverage": "drinks", "water": "drinks", "tea": "drinks", "coffee": "drinks",
    "milk": "dairy", "butter": "dairy", "cheese": "dairy", "curd": "dairy",
    "paneer": "dairy", "yogurt": "dairy", "ghee": "dairy", "cream": "dairy",
    "noodle": "ready-to-eat", "instant": "ready-to-eat", "soup": "ready-to-eat",
    "pasta": "ready-to-eat", "sauce": "ready-to-eat", "pickle": "ready-to-eat",
    "chocolate": "meetha", "candy": "meetha", "sweet": "meetha", "toffee": "meetha",
    "mithai": "meetha", "ladoo": "meetha", "barfi": "meetha",
    "cereal": "nashta", "oat": "nashta", "muesli": "nashta", "breakfast": "nashta",
    "cornflake": "nashta", "granola": "nashta", "poha": "nashta",
    "health drink": "bachon-ke-liye", "malt": "bachon-ke-liye", "bournvita": "bachon-ke-liye",
    "horlicks": "bachon-ke-liye", "complan": "bachon-ke-liye", "boost": "bachon-ke-liye",
    "baby": "bachon-ke-liye", "infant": "bachon-ke-liye",
    "bread": "nashta", "jam": "nashta", "spread": "nashta", "honey": "nashta",
    "oil": "cooking", "masala": "cooking", "spice": "cooking", "atta": "cooking",
    "dal": "cooking", "rice": "cooking", "flour": "cooking",
}

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text[:50].strip('-')

def get_category(product):
    name = product.get('product_name', '').lower()
    categories = product.get('categories', '').lower()
    combined = f"{name} {categories}"

    for keyword, category in CATEGORY_MAP.items():
        if keyword in combined:
            return category
    return "other"

def fetch_page(page, page_size=100):
    params = {
        'countries_tags_en': 'india',
        'states_tags': 'en:nutrition-facts-completed',
        'page': page,
        'page_size': page_size,
        'fields': 'code,product_name,brands,categories,nutriments,ingredients_text,quantity,image_url'
    }

    url = f"{API_BASE}?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'FoodAtEase/1.0 (https://foodatease.com)')
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('products', []), data.get('count', 0)
    except Exception as e:
        print(f"  Error fetching page {page}: {e}")
        return [], 0

def extract_nutrients(n):
    def get(key, default=0):
        v = n.get(f'{key}_100g', n.get(key, default))
        try:
            return round(float(v), 1) if v else default
        except:
            return default

    sodium = get('sodium')
    if sodium < 10:
        sodium *= 1000

    return {
        "energy_kcal": get('energy-kcal', get('energy', 0) / 4.184),
        "protein_g": get('proteins'),
        "carbohydrates_g": get('carbohydrates'),
        "sugar_g": get('sugars'),
        "total_fat_g": get('fat'),
        "saturated_fat_g": get('saturated-fat'),
        "fiber_g": get('fiber'),
        "sodium_mg": sodium,
    }

def is_valid(p):
    if not p.get('product_name'):
        return False
    name = p.get('product_name', '').lower()
    # Skip non-food
    skip = ['pet food', 'dog food', 'cat food', 'shampoo', 'soap', 'detergent', 'cosmetic']
    if any(s in name for s in skip):
        return False
    n = p.get('nutriments', {})
    return n.get('energy-kcal_100g') or n.get('energy_100g') or n.get('proteins_100g')

def process(p, slugs):
    name = p.get('product_name', '').strip()
    brand = p.get('brands', '').split(',')[0].strip() if p.get('brands') else ''

    # Clean name
    if brand and name.lower().startswith(brand.lower()):
        name = name[len(brand):].strip(' -:')
    name = re.sub(r'\s*\d{8,}', '', name)
    name = re.sub(r'\s*\d+\s*(g|ml|kg|l|pack|pcs?)(\s|$)', ' ', name, flags=re.I)
    name = re.sub(r'\s+', ' ', name).strip()

    full_name = f"{brand} {name}".strip() if brand else name
    if not full_name:
        full_name = f"Product {p.get('code', 'unknown')}"

    base_slug = slugify(full_name) or f"product-{p.get('code', 'x')}"
    slug = base_slug
    i = 1
    while slug in slugs:
        slug = f"{base_slug}-{i}"
        i += 1
    slugs.add(slug)

    nutrients = extract_nutrients(p.get('nutriments', {}))
    category = get_category(p)

    qty = p.get('quantity', '100')
    match = re.search(r'(\d+)', str(qty))
    pkg_size = int(match.group(1)) if match else 100

    ingredients = p.get('ingredients_text', '')
    ingredients_list = [i.strip() for i in ingredients.split(',')[:12]] if ingredients else []

    flags = []
    if nutrients['sodium_mg'] > 500:
        flags.append("High Sodium")
    if nutrients['sugar_g'] > 15:
        flags.append("High Sugar")
    if nutrients['saturated_fat_g'] > 5:
        flags.append("High Saturated Fat")

    return {
        "id": p.get('code', slug),
        "slug": slug,
        "name": full_name,
        "brand": brand or "Unknown",
        "category": category.replace('-', ' ').title(),
        "category_slug": category,
        "package_size_g": pkg_size,
        "nutrients": nutrients,
        "ingredients": ingredients_list,
        "flags": flags,
        "image_url": p.get('image_url', ''),
        "source": "Open Food Facts",
    }

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=0, help='Max products (0=all)')
    parser.add_argument('--start-page', type=int, default=1)
    args = parser.parse_args()

    products = []
    slugs = set()
    seen = set()
    counts = defaultdict(int)

    # First, get total count
    _, total = fetch_page(1, 1)
    print(f"🎯 Total available: {total} Indian products with nutrition data")

    if args.limit:
        target = min(args.limit, total)
        print(f"📦 Fetching up to {target} products...")
    else:
        target = total
        print(f"📦 Fetching ALL {total} products...")

    page = args.start_page
    page_size = 100

    while len(products) < target:
        print(f"\n📄 Page {page} (have {len(products)}/{target})...")

        results, _ = fetch_page(page, page_size)
        if not results:
            print("  No more results")
            break

        added = 0
        for p in results:
            if len(products) >= target:
                break

            code = p.get('code')
            if code in seen or not is_valid(p):
                continue
            seen.add(code)

            try:
                product = process(p, slugs)
                products.append(product)
                counts[product['category_slug']] += 1
                added += 1
            except Exception as e:
                pass

        print(f"  Added {added} products")
        page += 1
        time.sleep(0.5)  # Rate limiting

    # Save
    output = Path(__file__).parent.parent / "src" / "data" / "products_raw.json"
    data = {
        "source": "Open Food Facts",
        "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(products),
        "products": products
    }

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Total: {len(products)} products")
    print("\n📊 By category:")
    for cat, count in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    print(f"\n💾 Saved to: {output}")

if __name__ == "__main__":
    main()
