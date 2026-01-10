# NutriWatch India: The Definitive Plan

## A Searchable Directory of Packaged Foods with Honest Health Ratings

---

# PART I: WHAT WE'RE ACTUALLY BUILDING

## The Concept (Crystal Clear)

**NutriWatch is a website — a searchable directory of packaged food products sold in India.**

Think:
- **IMDB for food** — every product has a detailed page
- **Zomato, but for nutrition** — search, browse, compare
- **Google, but only for packaged foods** — "maggi nutrition" lands you on our page

**What it is NOT:**
- ❌ Not a mobile app
- ❌ Not a barcode scanner
- ❌ Not real-time image analysis
- ❌ Not something users need to download

**What it IS:**
- ✅ A static website (fast, cheap, SEO-friendly)
- ✅ A searchable database of 10,000+ Indian products
- ✅ Pre-computed health scores, warnings, and "roasts"
- ✅ Automated backend that keeps data fresh
- ✅ 100% open source

---

## User Journey (Simple)

```
USER WANTS TO KNOW: "Is Bournvita actually healthy?"

STEP 1: Google search → "bournvita health rating"
        or
        Direct visit → nutriwatch.in → Search "Bournvita"

STEP 2: Lands on product page:
        nutriwatch.in/product/bournvita-chocolate-health-drink-500g

STEP 3: Sees everything:
        • Star rating (2.5/5)
        • What's actually in it (39% sugar)
        • Safe daily limit (2 spoons before you hit sugar cap)
        • The "Roast" (brutal honest take)
        • Comparison to alternatives
        • Additives flagged

STEP 4: Makes informed decision. Shares link with family WhatsApp group.
```

No app. No scan. No friction. Just information.

---

## Site Structure

```
nutriwatch.in/
│
├── /                           → Homepage (search bar, featured, trending)
├── /search?q=maggi             → Search results
├── /product/[slug]             → Individual product page (the core)
├── /category/[category]        → Browse by category
├── /brand/[brand]              → All products from a brand
├── /compare?p=123&p=456        → Side-by-side comparison
├── /worst                      → Hall of shame (worst rated)
├── /best                       → Actually healthy options
├── /learn                      → Educational content
└── /about                      → Mission, methodology, team
```

---

## The Product Page (Core Experience)

This is where the magic happens. Every product page answers:

```
┌─────────────────────────────────────────────────────────────────┐
│  BOURNVITA CHOCOLATE HEALTH DRINK                               │
│  Cadbury | 500g | ₹235                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ██████████░░░░░░░░░░  2.5 / 5 STARS                           │
│                                                                 │
│  "Health drink" — but 39% sugar                                 │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ⚠️  SAFE LIMIT: 20g per day (2 level spoons)                   │
│                                                                 │
│  WHY? At 2 spoons, you've consumed:                             │
│  • 7.8g sugar (16% of daily limit)                              │
│  • Only 2.4g protein (you wanted 15g+)                          │
│                                                                 │
│  The jar lasts 25 days at safe consumption.                     │
│  Most families finish it in 10 days. That's 2.5x overconsumption│
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📊 NUTRITION BREAKDOWN (per 100g)                              │
│                                                                 │
│  Energy      390 kcal    ████████████████░░░░  High             │
│  Sugar       39.0g       ████████████████████  CRITICAL         │
│  Protein     7.0g        ████░░░░░░░░░░░░░░░░  Low              │
│  Fat         2.0g        ██░░░░░░░░░░░░░░░░░░  OK               │
│  Sodium      150mg       ███░░░░░░░░░░░░░░░░░  OK               │
│  Fiber       0g          ░░░░░░░░░░░░░░░░░░░░  None             │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🔬 INGREDIENT ANALYSIS                                         │
│                                                                 │
│  #1: Sugar              ← This is the main ingredient           │
│  #2: Malted Barley      ← Basically more sugar                  │
│  #3: Cocoa Solids                                               │
│  #4: Wheat Flour        ← Carbs, not protein                    │
│  ...                                                            │
│  #7: Milk Solids        ← Finally, some nutrition               │
│                                                                 │
│  ⚠️ FLAGS:                                                      │
│  • "Hidden Sugar" — Maltodextrin detected                       │
│  • NOVA Group 4 — Ultra-processed                               │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  💀 THE ROAST                                                   │
│                                                                 │
│  "You're paying ₹235 to add sugar to milk and call it           │
│  'brain food.' The protein claims on the jar? Mostly from       │
│  the milk you're adding anyway. Ingredient #1 is literally      │
│  sugar. The kid in the advertisement grew up despite this       │
│  product, not because of it."                                   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🔄 HEALTHIER ALTERNATIVES                                      │
│                                                                 │
│  • Sattu (roasted gram flour) — 20g protein, 0g added sugar     │
│  • Plain milk + 1 boiled egg — 14g protein, ₹15                 │
│  • Homemade ragi malt — 7g protein, no additives                │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📱 SHARE THIS PAGE                                             │
│  [WhatsApp] [Copy Link] [Twitter]                               │
│                                                                 │
│  "My family needs to see this"                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

# PART II: TECHNICAL ARCHITECTURE (REFINED)

## The Stack (Truly Free, Truly Simple)

```
┌─────────────────────────────────────────────────────────────────┐
│                         USERS                                   │
│                           │                                     │
│              Google Search / Direct Visit                       │
│                           │                                     │
│                           ▼                                     │
├─────────────────────────────────────────────────────────────────┤
│                    GITHUB PAGES                                 │
│                  (Static Site Host)                             │
│                                                                 │
│   • Free unlimited bandwidth                                    │
│   • Global CDN (fast in India)                                  │
│   • Custom domain support                                       │
│   • HTTPS included                                              │
├─────────────────────────────────────────────────────────────────┤
│                    STATIC SITE                                  │
│               (Astro / Next.js SSG)                             │
│                                                                 │
│   • Pre-rendered HTML for every product                         │
│   • Client-side search (Fuse.js / Pagefind)                     │
│   • No server needed                                            │
│   • SEO-optimized (each page rankable on Google)                │
├─────────────────────────────────────────────────────────────────┤
│                    DATA LAYER                                   │
│                  (JSON in Repo)                                 │
│                                                                 │
│   products.json      — Master product database                  │
│   categories.json    — Category taxonomy                        │
│   additives.json     — Additive blocklist + info                │
│   search-index.json  — Pre-built search index                   │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
              AUTOMATED UPDATES (Weekly)
                              │
┌─────────────────────────────────────────────────────────────────┐
│                   GITHUB ACTIONS                                │
│                  (Cron: Tue/Fri 3AM)                            │
│                                                                 │
│   1. Fetch new products from Open Food Facts API                │
│   2. Filter for India (country tag + barcode 890)               │
│   3. For products with images but no nutrition:                 │
│      → Send to Gemini 2.0 Flash for extraction                  │
│   4. Calculate health scores (INR algorithm)                    │
│   5. Generate roasts (Gemini with persona prompt)               │
│   6. Update products.json                                       │
│   7. Rebuild static site                                        │
│   8. Deploy to GitHub Pages                                     │
└─────────────────────────────────────────────────────────────────┘
```

## Why This Architecture Wins

| Benefit | Explanation |
|---------|-------------|
| **$0 hosting** | GitHub Pages is free for public repos |
| **Blazing fast** | Static HTML, global CDN, no database queries |
| **SEO goldmine** | Every product page is indexable by Google |
| **Scales infinitely** | 10 users or 10 million — same cost ($0) |
| **No server maintenance** | Nothing to crash, nothing to patch |
| **Works offline** | PWA caching for repeat visitors |
| **Forkable** | Anyone can clone and run their own version |

---

## Data Pipeline (Detailed)

### Step 1: Seed from Open Food Facts

```python
# seed_database.py (runs once, then incrementally)

import requests
import json

def fetch_indian_products():
    """
    Open Food Facts has 15,000+ Indian products.
    We fetch products where:
    - countries_tags contains 'india' OR
    - barcode starts with '890' (India GS1 prefix)
    """
    
    base_url = "https://world.openfoodfacts.org/cgi/search.pl"
    
    params = {
        'action': 'process',
        'tagtype_0': 'countries',
        'tag_contains_0': 'contains',
        'tag_0': 'india',
        'json': 1,
        'page_size': 100,
        'fields': 'code,product_name,brands,categories,nutriments,ingredients_text,image_url,nova_group'
    }
    
    all_products = []
    page = 1
    
    while True:
        params['page'] = page
        response = requests.get(base_url, params=params)
        data = response.json()
        
        products = data.get('products', [])
        if not products:
            break
            
        all_products.extend(products)
        page += 1
        
        # Rate limiting - be nice to OFF servers
        time.sleep(1)
    
    return all_products
```

### Step 2: Enrich with Gemini (for incomplete data)

```python
# enrich_products.py

import google.generativeai as genai

SYSTEM_PROMPT = """
You are a precise nutritional data extractor AND a cynical Indian nutritionist.

TASK 1: Extract nutrition data from the product image.
Return per 100g values. If only "per serving" shown, calculate per 100g.

TASK 2: Identify problematic ingredients:
- Hidden sugars (maltodextrin, corn syrup, etc.)
- Banned-in-EU additives still used in India
- Ultra-processing markers

TASK 3: Write "The Roast" - a 2-3 sentence brutal truth about this product.
Be witty but factual. Reference the Indian context (diabetes epidemic, 
hypertension rates, child nutrition crisis).

OUTPUT: JSON only, no markdown.
"""

def enrich_product(product):
    """
    For products with images but incomplete nutrition data,
    use Gemini to extract from label image.
    """
    
    if product.get('nutrients_complete'):
        return product  # Already have data
    
    if not product.get('image_url'):
        return product  # Can't do anything without image
    
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    response = model.generate_content([
        SYSTEM_PROMPT,
        {"image_url": product['image_url']},
        f"Product: {product.get('product_name', 'Unknown')}"
    ])
    
    try:
        extracted = json.loads(response.text)
        product['nutrients'] = extracted.get('nutrients', {})
        product['roast'] = extracted.get('roast', '')
        product['flags'] = extracted.get('flags', [])
        product['enriched_by_ai'] = True
    except:
        product['enriched_by_ai'] = False
    
    return product
```

### Step 3: Calculate Health Scores

```python
# calculate_scores.py

def calculate_inr_score(product):
    """
    Indian Nutrition Rating (INR) based on FSSAI draft guidelines.
    Returns 0.5 to 5 stars.
    """
    
    nutrients = product.get('nutrients', {})
    
    # Baseline points (bad stuff) - per 100g
    energy_points = get_energy_points(nutrients.get('energy_kcal', 0))
    sat_fat_points = get_satfat_points(nutrients.get('saturated_fat', 0))
    sugar_points = get_sugar_points(nutrients.get('sugars', 0))
    sodium_points = get_sodium_points(nutrients.get('sodium', 0))
    
    baseline = energy_points + sat_fat_points + sugar_points + sodium_points
    
    # Modifying points (good stuff)
    protein_points = get_protein_points(nutrients.get('protein', 0))
    fiber_points = get_fiber_points(nutrients.get('fiber', 0))
    fvnl_points = get_fvnl_points(product.get('ingredients', ''))
    
    # FSSAI rule: if baseline >= 13 and low FVNL, protein doesn't count
    if baseline >= 13 and fvnl_points < 5:
        modifying = fvnl_points + fiber_points  # No protein credit
    else:
        modifying = protein_points + fiber_points + fvnl_points
    
    final_score = baseline - modifying
    
    # Map to stars (lower score = more stars)
    stars = score_to_stars(final_score)
    
    return {
        'stars': stars,
        'baseline_points': baseline,
        'modifying_points': modifying,
        'limiting_factor': get_limiting_factor(nutrients)
    }


def calculate_safe_limit(product):
    """
    How much can you eat before hitting daily limits?
    Based on ICMR-NIN 2024 guidelines.
    """
    
    nutrients = product.get('nutrients', {})
    
    # Daily limits for Indians (ICMR 2024)
    DAILY_LIMITS = {
        'sodium': 2000,      # mg
        'added_sugar': 50,   # g (stricter than WHO's 50g)
        'saturated_fat': 22, # g (for 2000 kcal diet)
        'trans_fat': 2.2,    # g (should be zero ideally)
    }
    
    # Calculate how many grams to hit each limit
    limits = {}
    
    for nutrient, daily_max in DAILY_LIMITS.items():
        per_100g = nutrients.get(nutrient, 0)
        if per_100g > 0:
            grams_to_hit_limit = (100 * daily_max) / per_100g
            limits[nutrient] = grams_to_hit_limit
    
    if not limits:
        return None
    
    # The limiting factor is whichever you hit first
    limiting_nutrient = min(limits, key=limits.get)
    max_grams = limits[limiting_nutrient]
    
    # Safe snack = 15% of daily allowance
    safe_snack = max_grams * 0.15
    
    return {
        'max_daily_grams': round(max_grams),
        'safe_snack_grams': round(safe_snack),
        'limiting_nutrient': limiting_nutrient,
        'explanation': generate_limit_explanation(limiting_nutrient, max_grams, nutrients)
    }


def generate_limit_explanation(nutrient, max_grams, nutrients):
    """Human-readable explanation of the limit."""
    
    explanations = {
        'sodium': f"At {round(max_grams)}g, you hit 100% of your daily sodium. "
                  f"That's your entire salt allowance for the day gone.",
        'added_sugar': f"At {round(max_grams)}g, you max out daily sugar. "
                       f"Save room for the sugar hiding in everything else you'll eat.",
        'saturated_fat': f"At {round(max_grams)}g, you've consumed all the saturated fat "
                         f"your arteries can handle today.",
        'trans_fat': f"At {round(max_grams)}g, you've consumed the WHO limit for trans fat. "
                     f"This should be zero. Any amount damages your heart."
    }
    
    return explanations.get(nutrient, f"Limited by {nutrient}")
```

### Step 4: Build the Static Site

```javascript
// astro.config.mjs (using Astro for static generation)

import { defineConfig } from 'astro/config';

export default defineConfig({
  output: 'static',
  build: {
    format: 'directory'  // /product/maggi/ instead of /product/maggi.html
  },
  site: 'https://nutriwatch.in',
});
```

```astro
---
// src/pages/product/[slug].astro

import products from '../../data/products.json';
import ProductPage from '../../components/ProductPage.astro';

export async function getStaticPaths() {
  return products.map(product => ({
    params: { slug: product.slug },
    props: { product }
  }));
}

const { product } = Astro.props;
---

<ProductPage product={product} />
```

---

## GitHub Actions Workflow

```yaml
# .github/workflows/update-database.yml

name: Update Product Database

on:
  schedule:
    # Tuesday and Friday at 3 AM IST (9:30 PM UTC previous day)
    - cron: '30 21 * * 1,4'
  workflow_dispatch:  # Manual trigger

jobs:
  update:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install requests google-generativeai
      
      - name: Fetch new products from Open Food Facts
        run: python scripts/fetch_new_products.py
        
      - name: Enrich incomplete products with Gemini
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python scripts/enrich_products.py
        
      - name: Calculate health scores
        run: python scripts/calculate_scores.py
        
      - name: Generate search index
        run: python scripts/build_search_index.py
      
      - name: Build static site
        run: |
          npm ci
          npm run build
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

---

## Cost Breakdown (Final)

| Service | What For | Monthly Cost |
|---------|----------|--------------|
| GitHub Pages | Hosting | $0 |
| GitHub Actions | CI/CD (2000 mins free) | $0 |
| Gemini API | AI enrichment (~500 products/week) | $0-3 |
| Domain | nutriwatch.in | ~$1 (₹800/year) |
| **TOTAL** | | **<$5/month** |

At scale (100K+ daily visitors), still $0 for hosting. Static sites don't care about traffic.

---

# PART III: THE DIALOGUE (REFINED)

## Scene 2: "The Directory"

---

**SETTING:** Same auditorium. Product launch. PRIYA on stage. Large screen behind her.

---

**PRIYA:**
Six months ago, Dr. Mehta asked me what I was going to build.

*(She clicks. A clean website interface appears on screen.)*

This is NutriWatch. A website. Not an app. Not something you download. A website.

*(She types into the search bar on screen: "Maggi")*

Let's say you're a mother. Your kid wants Maggi for dinner. You've heard... things. But you're not sure. The packet looks the same as it did when you were a kid.

So you Google "Maggi nutrition" or "is Maggi healthy" — and you land here.

*(The product page loads)*

---

**PRIYA:**
What you see is everything the company doesn't want on the front of the packet.

*(She points to the screen)*

**1.5 stars.** Out of 5. Based on the same rating system the government is about to mandate — we just implemented it first.

**Safe limit: 45 grams.** That's half the packet. The packet most people finish in one sitting.

And then... the roast.

*(She reads from screen)*

"Maggi: teaching Indian children that dinner can be ready in 2 minutes and your sodium can be maxed out in 4 bites. That 'tastemaker' packet? Contains 72% of an adult's daily salt. For a child, it's worse. But hey, at least it's 'made with love' — and monosodium glutamate."

*(Scattered uncomfortable laughter)*

---

**PRIYA:**
This isn't a scandal. This isn't an exposé. Every single number on this page comes from Maggi's own nutrition label.

We just did the math.

We translated "Sodium: 1060mg per 100g" into "This is half your day's salt in half a packet."

We're not telling you anything new. We're telling you what was always there — in a language you can actually understand.

---

*(She types another search: "Bournvita")*

**PRIYA:**
Let's try something marketed as healthy.

*(Page loads)*

Bournvita. "Tayyari jeet ki." Preparation for victory. The advertisement shows a kid becoming a champion.

What's actually in it?

*(She scrolls)*

**Ingredient number one: Sugar.**

Not milk solids. Not vitamins. Sugar.

39% of this jar is sugar. When you add two spoons to your child's milk, you're adding 8 grams of sugar and calling it nutrition.

You know what's a better source of protein? The milk itself. Without the ₹235 chocolate-flavored sugar delivery system.

---

**VOICE FROM AUDIENCE:**
But where does this data come from? How do we know it's accurate?

**PRIYA:**
*(nodding)*
Fair question.

Three sources:

**One:** Open Food Facts — an international open-source database with 15,000+ Indian products, contributed by volunteers worldwide.

**Two:** The products' own labels. We use AI to read nutrition panels from product images when the data isn't available.

**Three:** The Indian government's own guidelines. The star ratings use the exact formula from FSSAI's draft Indian Nutrition Rating. The daily limits come from the 2024 ICMR guidelines.

Every calculation is documented. Every algorithm is public. You can literally read the code that generates these numbers.

*(She clicks to the GitHub page)*

It's all here. Open source. MIT license. If we made a mistake, you can fix it yourself and submit a correction.

---

**PRIYA:**
Here's what makes this different from every "health app" that came before.

*(She brings up a comparison)*

There is no premium tier. No ₹299/month subscription. No "unlock detailed analysis."

The information is free. Forever. For everyone.

A mother in Mumbai and a mother in Muzaffarpur see the exact same data.

Why? Because health information shouldn't be a luxury. Understanding what you feed your children shouldn't require a medical degree or a credit card.

---

**PRIYA:**
We have 12,000 products in the database today. Every major brand. Every category from biscuits to baby food.

*(She pulls up the category page)*

You can browse by category: "Show me all breakfast cereals ranked by health rating."

*(The list appears — Kellogg's Chocos near the bottom, plain oats at the top)*

You can browse by brand: "Show me everything made by Britannia, ranked."

*(Another list — some products 4 stars, some 1.5)*

You can search by what you're avoiding: "Show me snacks with no added sugar."

*(A shorter, sadder list appears)*

*(Wry smile)*

That last search returns... not many results. Which tells you something about the state of Indian packaged food.

---

**PRIYA:**
The goal isn't to make you stop eating everything.

*(She brings up a "Best In Category" page)*

The goal is to make better choices visible.

Look — these are biscuits that scored 3.5 stars or higher. They exist. They're in the same stores. They cost about the same.

You just couldn't tell them apart from the 1-star options because they all have the same "healthy" marketing.

Now you can.

---

**PRIYA:**
Every product page has a share button. One click — it's on your family WhatsApp group.

*(She demos it)*

"My mother-in-law kept giving my kid this 'health drink.' I sent her the NutriWatch link. She stopped."

"I showed my husband the page for his favorite namkeen. He didn't believe me until he saw it. Now we buy a different brand."

That's how change happens. Not through government mandates that take years. Not through lawsuits that take decades.

Through information. Shared at scale. By people who care about each other.

---

**PRIYA:**
*(Pausing, looking at the audience)*

I want to be clear about something.

This website won't solve child malnutrition. It won't fix the fact that 57% of Indian women are anemic. It won't reverse decades of damage.

But it might help a mother make a slightly better choice at the grocery store tomorrow.

Multiply that by millions of mothers. Millions of choices. Over years.

That adds up.

---

**PRIYA:**
We're open source. That means we're asking for help.

*(She brings up the GitHub contributors page)*

Right now, we have 43 contributors. Developers who wrote code. Nutritionists who verified our algorithms. Medical students who researched additives. Translators who are working on Hindi, Tamil, Telugu.

We need more.

If you can code — we need better search, better mobile experience, better accessibility.

If you know nutrition — we need people to verify our scoring against clinical literature.

If you speak a regional language — we need translations. A mother in rural Karnataka shouldn't need English to understand this.

And if you can't do any of that — just share the site. That's contribution enough.

---

**PRIYA:**
*(Final beat, looking at Dr. Mehta)*

Six months ago, you told us India had a hidden health crisis.

This doesn't fix it. But it makes it a little less hidden.

One product at a time. One family at a time.

*(She gestures to the screen)*

NutriWatch.in.

Go see what you've been eating.

---

**FADE TO BLACK.**

---

## POST-CREDITS TEXT:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NUTRIWATCH INDIA
nutriwatch.in

12,000+ products
100% free
Open source forever

github.com/nutriwatch-india

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Every statistic in this film is real.
Every product rating uses published formulas.
Every line of code is public.

The information was always on the label.
We just made it readable.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

# PART IV: IMPLEMENTATION ROADMAP

## Phase 1: Foundation (Weeks 1-2)
- [ ] Set up GitHub repository with MIT license
- [ ] Import Open Food Facts Indian products (~15,000)
- [ ] Build data cleaning pipeline
- [ ] Implement INR scoring algorithm
- [ ] Basic Astro site with product pages

## Phase 2: Intelligence (Weeks 3-4)
- [ ] Integrate Gemini for missing data enrichment
- [ ] Implement "Safe Limit" calculations
- [ ] Add "Roast" generation
- [ ] Build additive flagging system
- [ ] Set up GitHub Actions cron job

## Phase 3: Experience (Weeks 5-6)
- [ ] Implement client-side search (Pagefind)
- [ ] Build category/brand browse pages
- [ ] Add comparison feature
- [ ] Create "Worst" and "Best" rankings
- [ ] Mobile optimization (PWA)

## Phase 4: Launch (Week 7)
- [ ] Beta testing with select users
- [ ] SEO optimization for product pages
- [ ] Social sharing optimization (OG images)
- [ ] Write documentation for contributors
- [ ] Public launch

## Phase 5: Scale (Ongoing)
- [ ] Hindi translation
- [ ] Regional language expansion
- [ ] Community scan-a-thons
- [ ] Partnership with nutrition organizations
- [ ] Integration with Open Food Facts contribution

---

# PART V: OPEN SOURCE ASSETS

## README.md Template

```markdown
# 🥗 NutriWatch India

**The open-source directory of packaged foods with honest health ratings.**

[Visit Site](https://nutriwatch.in) | [View Products](https://nutriwatch.in/browse) | [Contribute](#contributing)

---

## What is this?

NutriWatch is a free, searchable database of 12,000+ packaged food products sold in India. Each product has:

- ⭐ **Health Star Rating** (based on FSSAI's Indian Nutrition Rating formula)
- ⚠️ **Safe Daily Limit** ("Stop at 27 grams — that's 2 tablespoons")
- 💀 **The Roast** (a brutally honest take on what this product does to your body)
- 🚫 **Additive Alerts** (ingredients banned in EU but legal in India)
- 📊 **Full Nutrition Breakdown** (with visual indicators)

## Why?

- 73% of Indians are protein deficient
- 57% of Indian women are anemic
- 89 million Indians have diabetes
- Most people can't decode nutrition labels

Information shouldn't require a medical degree.

## Tech Stack

- **Site**: Astro (static generation)
- **Hosting**: GitHub Pages (free)
- **Data**: Open Food Facts + AI enrichment
- **AI**: Gemini 2.0 Flash
- **Search**: Pagefind (client-side)
- **CI/CD**: GitHub Actions

**Monthly cost: <$5**

## Contributing

We need help with:

- 🌐 **Translations** — Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Marathi, Gujarati
- 📸 **Data** — Add products not in our database
- 💻 **Code** — See open issues
- 🔬 **Verification** — Medical/nutrition experts to validate algorithms
- 📢 **Spreading the word** — Share with family and friends

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT — Free forever. Fork it. Improve it. Save lives.

---

*Made with ❤️ for India's 1.4 billion people.*
```

---

*End of Document*
