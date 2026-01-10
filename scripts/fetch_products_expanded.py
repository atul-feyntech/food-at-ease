#!/usr/bin/env python3
"""
Mizan Expanded Product Fetcher
Fetches diverse Indian packaged foods from Open Food Facts.
Covers all major categories and brands.
"""

import json
import urllib.request
import urllib.parse
import time
import re
from pathlib import Path
from collections import defaultdict

OFF_API_BASE = "https://world.openfoodfacts.org"

# Comprehensive list of Indian brands by category
BRANDS_BY_CATEGORY = {
    "biscuits": [
        "Parle", "Britannia", "ITC Sunfeast", "Unibic", "Anmol", "Priyagold",
        "Cremica", "Dukes", "McVities", "Oreo", "Cadbury", "Lotus"
    ],
    "namkeen": [
        "Haldiram", "Bikano", "Balaji", "Bikanervala", "Prabhuji", "Chitale",
        "Cornitos", "Too Yumm", "Kurkure", "Lay's", "Bingo", "Uncle Chipps",
        "Pringles", "Doritos", "Act II"
    ],
    "noodles": [
        "Maggi", "Yippee", "Top Ramen", "Wai Wai", "Ching's", "Knorr",
        "Nissin", "Patanjali", "Smith & Jones"
    ],
    "drinks": [
        "Coca-Cola", "Pepsi", "Thums Up", "Sprite", "Fanta", "Limca",
        "Maaza", "Frooti", "Slice", "Appy", "Real", "Tropicana",
        "Paper Boat", "Raw Pressery", "B Natural", "Dabur",
        "Red Bull", "Monster", "Sting", "Glucon-D", "Tang", "Rasna"
    ],
    "dairy": [
        "Amul", "Mother Dairy", "Nestle", "Britannia", "Go Cheese",
        "Milky Mist", "Chitale", "Nandini", "Verka", "Vijaya"
    ],
    "chocolate": [
        "Cadbury", "Nestle", "Ferrero", "Mars", "Hershey", "Lindt",
        "Amul", "Campco", "Fabelle", "Snickers", "KitKat", "5 Star"
    ],
    "health_drinks": [
        "Bournvita", "Horlicks", "Complan", "Boost", "Protinex",
        "Ensure", "Pediasure", "Milo"
    ],
    "cereals": [
        "Kellogg's", "Quaker", "Bagrrys", "Saffola", "True Elements",
        "Muesli", "Yoga Bar", "Soulfull"
    ],
    "spreads": [
        "Nutella", "Kissan", "Veeba", "Dr. Oetker", "Funfoods",
        "Cremica", "Del Monte", "Heinz"
    ],
    "ready_to_eat": [
        "MTR", "Gits", "Haldiram", "ITC Kitchens of India", "Kohinoor",
        "Tasty Bite", "McCain", "Safal"
    ],
    "sauces": [
        "Maggi", "Kissan", "Heinz", "Del Monte", "Veeba", "Ching's",
        "Funfoods", "Cremica", "Tops"
    ],
    "pickles_chutneys": [
        "Mother's Recipe", "Priya", "Bedekar", "Tops", "Kissan"
    ]
}

# Additional search terms for variety
SEARCH_TERMS = [
    # Specific products
    "glucose biscuits india", "cream biscuits india", "digestive biscuits india",
    "masala chips india", "potato chips india", "namkeen mixture",
    "instant noodles india", "cup noodles india",
    "mango juice india", "orange juice india", "mixed fruit juice",
    "cola india", "lemon soda india", "energy drink india",
    "chocolate bar india", "milk chocolate india", "dark chocolate india",
    "cheese spread india", "butter india", "paneer india",
    "cornflakes india", "oats india", "muesli india",
    "tomato ketchup india", "chilli sauce india", "mayonnaise india",
    "pickle india", "chutney india",
    "health drink india", "protein powder india",
    # Categories
    "snacks india", "beverages india", "confectionery india",
    "breakfast cereals india", "instant food india"
]

CATEGORY_MAP = {
    "noodles": "ready-to-eat", "instant": "ready-to-eat", "pasta": "ready-to-eat",
    "biscuits": "biscuits", "cookies": "biscuits", "wafer": "biscuits",
    "chips": "namkeen", "snacks": "namkeen", "namkeen": "namkeen", "crisps": "namkeen",
    "beverages": "drinks", "drinks": "drinks", "juice": "drinks", "soda": "drinks",
    "cola": "drinks", "soft drink": "drinks", "energy": "drinks",
    "chocolate": "meetha", "candy": "meetha", "sweets": "meetha", "confectionery": "meetha",
    "dairy": "dairy", "milk": "dairy", "butter": "dairy", "cheese": "dairy",
    "yogurt": "dairy", "curd": "dairy", "paneer": "dairy",
    "cereal": "nashta", "breakfast": "nashta", "oats": "nashta", "muesli": "nashta",
    "spread": "nashta", "jam": "nashta",
    "health drink": "bachon-ke-liye", "malt": "bachon-ke-liye", "nutrition": "bachon-ke-liye",
    "sauce": "ready-to-eat", "ketchup": "ready-to-eat",
}

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text[:50]

def get_category(product_data):
    categories = product_data.get('categories', '').lower()
    product_name = product_data.get('product_name', '').lower()
    combined = f"{categories} {product_name}"

    for keyword, category in CATEGORY_MAP.items():
        if keyword in combined:
            return category
    return "namkeen"

def search_products(query, page=1, page_size=100):
    params = {
        'search_terms': query,
        'search_simple': 1,
        'action': 'process',
        'json': 1,
        'page': page,
        'page_size': page_size,
        'countries_tags_en': 'india',
        'fields': 'code,product_name,brands,categories,nutriments,serving_size,ingredients_text,image_url,quantity'
    }

    url = f"{OFF_API_BASE}/cgi/search.pl?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mizan/1.0 (https://mizan.live; contact@mizan.live)')

        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('products', [])
    except Exception as e:
        print(f"    Error: {e}")
        return []

def parse_quantity(quantity_str):
    if not quantity_str:
        return 100
    quantity_str = str(quantity_str).lower()
    match = re.search(r'(\d+(?:\.\d+)?)\s*(g|gm|gram|ml|l|kg)', quantity_str)
    if match:
        value = float(match.group(1))
        unit = match.group(2)
        if unit in ['kg', 'l']:
            return value * 1000
        return value
    return 100

def extract_nutrients(nutriments):
    def get_value(key, default=0):
        val = nutriments.get(f'{key}_100g', nutriments.get(key, default))
        try:
            return round(float(val), 1) if val else default
        except (ValueError, TypeError):
            return default

    sodium = get_value('sodium')
    if sodium < 10:  # Probably in grams, convert to mg
        sodium = sodium * 1000

    return {
        "energy_kcal": get_value('energy-kcal', get_value('energy', 0) / 4.184),
        "protein_g": get_value('proteins'),
        "carbohydrates_g": get_value('carbohydrates'),
        "sugar_g": get_value('sugars'),
        "total_fat_g": get_value('fat'),
        "saturated_fat_g": get_value('saturated-fat'),
        "fiber_g": get_value('fiber'),
        "sodium_mg": sodium,
    }

def is_valid_product(product):
    if not product.get('product_name'):
        return False
    name = product.get('product_name', '').lower()
    # Skip non-food items
    skip_terms = ['pet food', 'dog food', 'cat food', 'shampoo', 'soap', 'detergent']
    if any(term in name for term in skip_terms):
        return False

    nutriments = product.get('nutriments', {})
    has_energy = nutriments.get('energy-kcal_100g') or nutriments.get('energy_100g')
    has_other = any([
        nutriments.get('proteins_100g'),
        nutriments.get('sugars_100g'),
        nutriments.get('sodium_100g'),
        nutriments.get('fat_100g')
    ])
    return has_energy or has_other

def clean_product_name(name, brand):
    name = name.strip()
    # Remove brand from start if duplicated
    if brand and name.lower().startswith(brand.lower()):
        name = name[len(brand):].strip(' -:')
    # Remove product codes
    name = re.sub(r'\s*\d{8,}', '', name)
    # Remove size info
    name = re.sub(r'\s*\d+\s*(g|gm|ml|l|kg|pack|pcs?|x\s*\d+)(\s|$)', ' ', name, flags=re.I)
    # Clean up
    name = re.sub(r'\s+', ' ', name).strip()

    if brand and name:
        return f"{brand} {name}"
    return name or brand or "Unknown Product"

def process_product(off_product, existing_slugs):
    name = off_product.get('product_name', '').strip()
    brand = off_product.get('brands', '').split(',')[0].strip() if off_product.get('brands') else ''

    full_name = clean_product_name(name, brand)

    # Generate unique slug
    base_slug = slugify(full_name)
    if not base_slug:
        base_slug = f"product-{off_product.get('code', 'unknown')}"

    slug = base_slug
    counter = 1
    while slug in existing_slugs:
        slug = f"{base_slug}-{counter}"
        counter += 1
    existing_slugs.add(slug)

    nutrients = extract_nutrients(off_product.get('nutriments', {}))
    category = get_category(off_product)
    package_size = parse_quantity(off_product.get('quantity'))

    ingredients_text = off_product.get('ingredients_text', '')
    ingredients = [i.strip() for i in ingredients_text.split(',')[:15]] if ingredients_text else []

    flags = []
    if nutrients['sodium_mg'] > 500:
        flags.append("High Sodium")
    if nutrients['sugar_g'] > 15:
        flags.append("High Sugar")
    if nutrients['saturated_fat_g'] > 5:
        flags.append("High Saturated Fat")

    return {
        "id": off_product.get('code', slug),
        "slug": slug,
        "name": full_name,
        "brand": brand or "Unknown",
        "category": category.replace('-', ' ').title(),
        "category_slug": category,
        "package_size_g": package_size,
        "nutrients": nutrients,
        "ingredients": ingredients,
        "flags": flags,
        "image_url": off_product.get('image_url', ''),
        "source": "Open Food Facts",
        "source_url": f"https://world.openfoodfacts.org/product/{off_product.get('code', '')}"
    }

def fetch_all_products(target_count=200):
    products = []
    existing_slugs = set()
    seen_codes = set()
    category_counts = defaultdict(int)

    print(f"🎯 Target: {target_count} diverse Indian products\n")

    # Phase 1: Search by brand
    print("📦 Phase 1: Searching by brand...")
    for category, brands in BRANDS_BY_CATEGORY.items():
        if len(products) >= target_count:
            break
        print(f"\n  Category: {category}")
        for brand in brands:
            if len(products) >= target_count:
                break
            results = search_products(brand, page_size=50)
            added = 0
            for off_product in results:
                if len(products) >= target_count:
                    break
                code = off_product.get('code')
                if code in seen_codes:
                    continue
                seen_codes.add(code)

                if not is_valid_product(off_product):
                    continue

                try:
                    product = process_product(off_product, existing_slugs)
                    products.append(product)
                    category_counts[product['category_slug']] += 1
                    added += 1
                except Exception as e:
                    pass

            if added:
                print(f"    {brand}: +{added}")
            time.sleep(0.3)

    # Phase 2: Search by terms
    if len(products) < target_count:
        print(f"\n📦 Phase 2: Searching by terms ({len(products)}/{target_count})...")
        for term in SEARCH_TERMS:
            if len(products) >= target_count:
                break
            results = search_products(term, page_size=30)
            added = 0
            for off_product in results:
                if len(products) >= target_count:
                    break
                code = off_product.get('code')
                if code in seen_codes:
                    continue
                seen_codes.add(code)

                if not is_valid_product(off_product):
                    continue

                try:
                    product = process_product(off_product, existing_slugs)
                    products.append(product)
                    category_counts[product['category_slug']] += 1
                    added += 1
                except:
                    pass

            if added:
                print(f"    '{term}': +{added}")
            time.sleep(0.3)

    print(f"\n✅ Fetched {len(products)} products")
    print("\n📊 By category:")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"    {cat}: {count}")

    return products

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=200)
    parser.add_argument('--output', type=str, default=None)
    args = parser.parse_args()

    products = fetch_all_products(args.limit)

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(__file__).parent.parent / "src" / "data" / "products_raw.json"

    data = {
        "source": "Open Food Facts",
        "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(products),
        "products": products
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Saved to: {output_path}")

if __name__ == "__main__":
    main()
