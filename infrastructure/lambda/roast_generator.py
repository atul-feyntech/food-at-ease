"""
FoodAtEase Roast Generator - AWS Lambda Function
Generates AI roasts for products using Gemini REST API.
"""

import json
import boto3
import urllib.request
import urllib.error

# Initialize clients
secrets_client = boto3.client('secretsmanager', region_name='ap-south-1')
s3_client = boto3.client('s3', region_name='ap-south-1')

def get_secret(secret_name):
    """Retrieve secret from AWS Secrets Manager."""
    response = secrets_client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

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

def call_gemini_api(api_key, prompt):
    """Call Gemini API using REST."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [{"text": f"{SYSTEM_PROMPT}\n\n{prompt}"}]
            }
        ],
        "generationConfig": {
            "temperature": 0.8,
            "topP": 0.95,
            "maxOutputTokens": 500
        }
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            text = result['candidates'][0]['content']['parts'][0]['text']
            return text.strip()
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.read().decode()}")
        return None
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None

def generate_roast(api_key, product):
    """Generate a roast for a single product."""
    nutrients = product.get('nutrients', {})
    score = product.get('foodatease_score', {})

    context = f"""
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
"""

    prompt = f"""Based on this product data, write a witty FoodAtEase verdict:
{context}
Remember: Be factual, witty, and use Hinglish naturally. Output ONLY valid JSON."""

    try:
        response_text = call_gemini_api(api_key, prompt)
        if not response_text:
            return None

        # Clean up response
        text = response_text
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        text = text.strip()

        roast_data = json.loads(text)
        roast_data["approved"] = False
        return roast_data

    except json.JSONDecodeError as e:
        print(f"JSON decode error for {product['name']}: {e}")
        print(f"Raw response: {response_text[:200] if response_text else 'None'}")
        return None
    except Exception as e:
        print(f"Error generating roast for {product['name']}: {e}")
        return None

def lambda_handler(event, context):
    """
    Lambda handler for roast generation.

    Event can contain:
    - s3_bucket: S3 bucket containing products.json
    - s3_key: S3 key for products.json
    - product_slug: Generate roast for specific product
    - force: Regenerate even if approved
    """
    print(f"Event: {json.dumps(event)}")

    # Get API key from Secrets Manager
    api_key = get_secret('foodatease/gemini-api-key')

    # Get products data from S3 or event
    s3_bucket = event.get('s3_bucket')
    s3_key = event.get('s3_key', 'products.json')

    if s3_bucket:
        print(f"Loading products from s3://{s3_bucket}/{s3_key}")
        response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
        products_data = json.loads(response['Body'].read().decode('utf-8'))
        products = products_data.get('products', [])
    elif event.get('products_data'):
        products_data = event.get('products_data')
        if isinstance(products_data, str):
            products_data = json.loads(products_data)
        products = products_data.get('products', [])
    else:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'FoodAtEase Roast Generator Lambda',
                'usage': 'Pass s3_bucket/s3_key or products_data in event',
                'example': {
                    's3_bucket': 'foodatease-data-894140384556',
                    's3_key': 'products.json',
                    'product_slug': 'optional-specific-product',
                    'force': False
                }
            })
        }

    # Filter products
    product_slug = event.get('product_slug')
    force = event.get('force', False)

    results = []

    for product in products:
        # Filter by slug if specified
        if product_slug and product.get('slug') != product_slug:
            continue

        # Skip if already approved (unless force)
        if product.get('roast', {}).get('approved') and not force:
            print(f"Skipping {product['name']} (already approved)")
            continue

        print(f"Generating roast for: {product['name']}")
        roast = generate_roast(api_key, product)

        if roast:
            product['roast'] = roast
            results.append({
                'slug': product.get('slug'),
                'name': product.get('name'),
                'roast': roast
            })

    # Save back to S3 if we loaded from there
    if s3_bucket and results:
        print(f"Saving updated products to s3://{s3_bucket}/{s3_key}")
        products_data['products'] = products
        s3_client.put_object(
            Bucket=s3_bucket,
            Key=s3_key,
            Body=json.dumps(products_data, indent=2, ensure_ascii=False),
            ContentType='application/json'
        )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Generated {len(results)} roasts',
            'results': results,
            's3_updated': s3_bucket if results else None
        })
    }
