#!/usr/bin/env python3
"""
Fetch diverse products with balanced categories.
"""

import json
import urllib.request
import urllib.parse
import time
import re
from pathlib import Path
from collections import defaultdict

OFF_API = "https://world.openfoodfacts.org/cgi/search.pl"

# Target products per category
CATEGORY_TARGETS = {
    "biscuits": 30,
    "namkeen": 25,
    "drinks": 25,
    "dairy": 20,
    "ready-to-eat": 20,
    "meetha": 20,
    "nashta": 15,
    "bachon-ke-liye": 15,
}

# Search queries per category
CATEGORY_QUERIES = {
    "biscuits": ["parle biscuits", "britannia biscuits", "oreo", "mcvities", "hide seek", "good day", "marie gold", "bourbon", "cream biscuits", "digestive biscuits"],
    "namkeen": ["kurkure", "lays chips", "haldiram", "bikano", "balaji", "bingo chips", "uncle chipps", "pringles", "doritos", "namkeen mixture"],
    "drinks": ["coca cola india", "pepsi india", "frooti", "maaza", "real juice", "tropicana", "appy fizz", "sprite", "thums up", "paper boat"],
    "dairy": ["amul butter", "amul cheese", "mother dairy", "britannia cheese", "milk india", "curd india", "paneer"],
    "ready-to-eat": ["maggi noodles", "yippee", "top ramen", "wai wai", "mtr ready", "gits", "knorr soup", "cup noodles"],
    "meetha": ["cadbury dairy milk", "kitkat", "5 star", "munch", "perk", "ferrero rocher", "snickers", "gems", "eclairs"],
    "nashta": ["kelloggs india", "quaker oats", "muesli india", "cornflakes india", "chocos", "saffola oats"],
    "bachon-ke-liye": ["bournvita", "horlicks", "complan", "boost", "pediasure"],
}

CATEGORY_MAP = {
    "biscuit": "biscuits", "cookie": "biscuits", "wafer": "biscuits",
    "chips": "namkeen", "snack": "namkeen", "namkeen": "namkeen", "crisp": "namkeen", "kurkure": "namkeen",
    "juice": "drinks", "drink": "drinks", "soda": "drinks", "cola": "drinks", "beverage": "drinks",
    "milk": "dairy", "butter": "dairy", "cheese": "dairy", "curd": "dairy", "paneer": "dairy", "yogurt": "dairy",
    "noodle": "ready-to-eat", "instant": "ready-to-eat", "soup": "ready-to-eat", "pasta": "ready-to-eat",
    "chocolate": "meetha", "candy": "meetha", "sweet": "meetha", "toffee": "meetha",
    "cereal": "nashta", "oat": "nashta", "muesli": "nashta", "breakfast": "nashta", "cornflake": "nashta",
    "health drink": "bachon-ke-liye", "malt": "bachon-ke-liye", "bournvita": "bachon-ke-liye", "horlicks": "bachon-ke-liye",
}

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text[:50].strip('-')

def get_category(product, query_category):
    name = product.get('product_name', '').lower()
    categories = product.get('categories', '').lower()
    combined = f"{name} {categories}"

    for keyword, category in CATEGORY_MAP.items():
        if keyword in combined:
            return category
    return query_category

def search(query, page_size=30):
    params = {
        'search_terms': query,
        'search_simple': 1,
        'action': 'process',
        'json': 1,
        'page_size': page_size,
        'countries_tags_en': 'india',
        'fields': 'code,product_name,brands,categories,nutriments,ingredients_text,quantity'
    }
    url = f"{OFF_API}?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mizan/1.0')
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8')).get('products', [])
    except:
        return []

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
    n = p.get('nutriments', {})
    return n.get('energy-kcal_100g') or n.get('energy_100g') or n.get('proteins_100g')

def process(p, slugs, cat):
    name = p.get('product_name', '').strip()
    brand = p.get('brands', '').split(',')[0].strip() if p.get('brands') else ''

    if brand and name.lower().startswith(brand.lower()):
        name = name[len(brand):].strip(' -:')
    name = re.sub(r'\s*\d{8,}', '', name)
    name = re.sub(r'\s*\d+\s*(g|ml|kg|l|pack|pcs?)(\s|$)', ' ', name, flags=re.I)
    name = re.sub(r'\s+', ' ', name).strip()

    full_name = f"{brand} {name}".strip() if brand else name

    base_slug = slugify(full_name) or f"product-{p.get('code', 'x')}"
    slug = base_slug
    i = 1
    while slug in slugs:
        slug = f"{base_slug}-{i}"
        i += 1
    slugs.add(slug)

    nutrients = extract_nutrients(p.get('nutriments', {}))
    category = get_category(p, cat)

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
        "source": "Open Food Facts",
    }

def main():
    products = []
    slugs = set()
    seen = set()
    counts = defaultdict(int)

    print("🎯 Fetching diverse Indian products...\n")

    for cat, queries in CATEGORY_QUERIES.items():
        target = CATEGORY_TARGETS.get(cat, 20)
        print(f"📦 {cat} (target: {target})")

        for query in queries:
            if counts[cat] >= target:
                break

            results = search(query)
            added = 0

            for p in results:
                if counts[cat] >= target:
                    break

                code = p.get('code')
                if code in seen or not is_valid(p):
                    continue
                seen.add(code)

                try:
                    product = process(p, slugs, cat)
                    products.append(product)
                    counts[product['category_slug']] += 1
                    added += 1
                except:
                    pass

            if added:
                print(f"  {query}: +{added}")
            time.sleep(0.3)

        print(f"  ✓ {counts[cat]} products\n")

    # Save
    output = Path(__file__).parent.parent / "src" / "data" / "products_raw.json"
    data = {
        "source": "Open Food Facts",
        "fetched_at": time.strftime("%Y-%m-%d"),
        "count": len(products),
        "products": products
    }

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Total: {len(products)} products")
    print("\n📊 By category:")
    for cat, count in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    print(f"\n💾 Saved to: {output}")

if __name__ == "__main__":
    main()
