#!/usr/bin/env python3
"""
FoodAtEase Score Calculator
Implements FSSAI Indian Nutrition Rating (INR) algorithm
Based on ICMR-NIN 2024 guidelines

Usage:
    python scripts/calculate-scores.py [input_file] [output_file]

If no arguments provided:
    - Reads from src/data/products.json
    - Writes to src/data/products.json (in-place)
"""

import json
import sys
from pathlib import Path
from typing import TypedDict, Optional

# ICMR-NIN 2024 Daily Reference Values for Indian Adults
DAILY_LIMITS = {
    "energy_kcal": 2000,
    "sodium_mg": 2000,
    "sugar_g": 50,  # Free sugars limit (10% of energy)
    "saturated_fat_g": 22,  # <10% of energy
    "protein_g": 55,  # RDA for reference adult
    "fiber_g": 30,
}


class NutrientPoints(TypedDict):
    energy: int
    sodium: int
    sugar: int
    saturated_fat: int
    protein: int
    fiber: int


def calculate_baseline_points(nutrients: dict, per_100g: bool = True) -> int:
    """
    Calculate baseline (negative) points based on FSSAI INR algorithm.
    Higher baseline = worse nutritional profile.

    Points are calculated per 100g/100ml.
    """
    points = 0

    # Energy points (0-10)
    energy = nutrients.get("energy_kcal", 0)
    if energy <= 80:
        points += 0
    elif energy <= 160:
        points += 1
    elif energy <= 240:
        points += 2
    elif energy <= 320:
        points += 3
    elif energy <= 400:
        points += 4
    elif energy <= 480:
        points += 5
    elif energy <= 560:
        points += 6
    elif energy <= 640:
        points += 7
    elif energy <= 720:
        points += 8
    elif energy <= 800:
        points += 9
    else:
        points += 10

    # Sodium points (0-10)
    sodium = nutrients.get("sodium_mg", 0)
    if sodium <= 90:
        points += 0
    elif sodium <= 180:
        points += 1
    elif sodium <= 270:
        points += 2
    elif sodium <= 360:
        points += 3
    elif sodium <= 450:
        points += 4
    elif sodium <= 540:
        points += 5
    elif sodium <= 630:
        points += 6
    elif sodium <= 720:
        points += 7
    elif sodium <= 810:
        points += 8
    elif sodium <= 900:
        points += 9
    else:
        points += 10

    # Sugar points (0-10)
    sugar = nutrients.get("sugar_g", 0)
    if sugar <= 4.5:
        points += 0
    elif sugar <= 9:
        points += 1
    elif sugar <= 13.5:
        points += 2
    elif sugar <= 18:
        points += 3
    elif sugar <= 22.5:
        points += 4
    elif sugar <= 27:
        points += 5
    elif sugar <= 31:
        points += 6
    elif sugar <= 36:
        points += 7
    elif sugar <= 40:
        points += 8
    elif sugar <= 45:
        points += 9
    else:
        points += 10

    # Saturated fat points (0-10)
    sat_fat = nutrients.get("saturated_fat_g", 0)
    if sat_fat <= 1:
        points += 0
    elif sat_fat <= 2:
        points += 1
    elif sat_fat <= 3:
        points += 2
    elif sat_fat <= 4:
        points += 3
    elif sat_fat <= 5:
        points += 4
    elif sat_fat <= 6:
        points += 5
    elif sat_fat <= 7:
        points += 6
    elif sat_fat <= 8:
        points += 7
    elif sat_fat <= 9:
        points += 8
    elif sat_fat <= 10:
        points += 9
    else:
        points += 10

    return points


def calculate_modifying_points(nutrients: dict) -> int:
    """
    Calculate modifying (positive) points for beneficial nutrients.
    Higher modifying points = better nutritional profile.
    """
    points = 0

    # Protein points (0-5)
    protein = nutrients.get("protein_g", 0)
    if protein <= 1.6:
        points += 0
    elif protein <= 3.2:
        points += 1
    elif protein <= 4.8:
        points += 2
    elif protein <= 6.4:
        points += 3
    elif protein <= 8.0:
        points += 4
    else:
        points += 5

    # Fiber points (0-5)
    fiber = nutrients.get("fiber_g", 0)
    if fiber <= 0.9:
        points += 0
    elif fiber <= 1.9:
        points += 1
    elif fiber <= 2.8:
        points += 2
    elif fiber <= 3.7:
        points += 3
    elif fiber <= 4.7:
        points += 4
    else:
        points += 5

    return points


def calculate_inr_score(nutrients: dict) -> tuple[int, int, int]:
    """
    Calculate the overall INR score.
    Returns (final_score, baseline_points, modifying_points)

    Final score range: -5 to 40
    Lower is better.
    """
    baseline = calculate_baseline_points(nutrients)
    modifying = calculate_modifying_points(nutrients)

    # Final score = baseline - modifying
    # Note: If baseline >= 11 and fruit/veg/nut < 80%, protein points don't count
    # Simplified: we assume most packaged foods don't have 80% fruit/veg
    final_score = baseline - modifying

    return final_score, baseline, modifying


def score_to_stars(inr_score: int) -> int:
    """
    Convert INR score to 1-5 star rating.
    Lower INR score = more stars.
    """
    if inr_score <= -1:
        return 5
    elif inr_score <= 2:
        return 4
    elif inr_score <= 10:
        return 3
    elif inr_score <= 18:
        return 2
    else:
        return 1


def score_to_grade(stars: int) -> str:
    """Convert star rating to letter grade."""
    grades = {5: "A", 4: "B", 3: "C", 2: "D", 1: "F"}
    return grades.get(stars, "F")


def get_limiting_factors(nutrients: dict) -> list[str]:
    """
    Identify which nutrients are the main concerns.
    Returns list of limiting factors with reasons.
    """
    factors = []

    sodium = nutrients.get("sodium_mg", 0)
    sugar = nutrients.get("sugar_g", 0)
    sat_fat = nutrients.get("saturated_fat_g", 0)
    energy = nutrients.get("energy_kcal", 0)

    # High sodium: >400mg per 100g
    if sodium > 400:
        factors.append(f"High sodium ({sodium}mg per 100g)")

    # High sugar: >15g per 100g
    if sugar > 15:
        factors.append(f"High sugar ({sugar}g per 100g)")

    # High saturated fat: >5g per 100g
    if sat_fat > 5:
        factors.append(f"High saturated fat ({sat_fat}g per 100g)")

    # High calories: >400kcal per 100g
    if energy > 400:
        factors.append(f"High calorie density ({energy}kcal per 100g)")

    return factors if factors else ["No major concerns"]


def calculate_safe_limit(nutrients: dict, package_size_g: float) -> dict:
    """
    Calculate the recommended daily serving limit based on ICMR guidelines.
    Returns safe limit info.
    """
    # Calculate how much of each daily limit 100g provides
    sodium_pct = (nutrients.get("sodium_mg", 0) / DAILY_LIMITS["sodium_mg"]) * 100
    sugar_pct = (nutrients.get("sugar_g", 0) / DAILY_LIMITS["sugar_g"]) * 100
    sat_fat_pct = (nutrients.get("saturated_fat_g", 0) / DAILY_LIMITS["saturated_fat_g"]) * 100
    energy_pct = (nutrients.get("energy_kcal", 0) / DAILY_LIMITS["energy_kcal"]) * 100

    # Find the most restrictive nutrient (highest % of daily limit per 100g)
    percentages = {
        "sodium": sodium_pct,
        "sugar": sugar_pct,
        "saturated_fat": sat_fat_pct,
        "calories": energy_pct
    }

    limiting_nutrient = max(percentages, key=percentages.get)
    limiting_pct = percentages[limiting_nutrient]

    # Calculate max grams before hitting 20% of any daily limit
    # We use 20% as a reasonable single-serving threshold
    if limiting_pct > 0:
        safe_serving_g = (20 / limiting_pct) * 100
    else:
        safe_serving_g = package_size_g  # No restriction needed

    # Cap at package size
    safe_serving_g = min(safe_serving_g, package_size_g)

    # Calculate daily percentages for the safe serving
    scale = safe_serving_g / 100

    daily_percentages = {
        "sodium": round(sodium_pct * scale, 1),
        "sugar": round(sugar_pct * scale, 1),
        "saturated_fat": round(sat_fat_pct * scale, 1),
        "calories": round(energy_pct * scale, 1)
    }

    # Generate explanation
    if safe_serving_g >= package_size_g:
        explanation = "You can eat the whole packet without exceeding recommended daily limits."
        explanation_hindi = "Pura packet kha sakte ho, daily limit cross nahi hogi."
    elif safe_serving_g < 30:
        explanation = f"Very limited portion recommended. Just {round(safe_serving_g)}g due to high {limiting_nutrient.replace('_', ' ')}."
        explanation_hindi = f"Bahut kam khana chahiye. Sirf {round(safe_serving_g)}g kyunki {limiting_nutrient.replace('_', ' ')} zyada hai."
    else:
        explanation = f"Limit to {round(safe_serving_g)}g to stay within {limiting_nutrient.replace('_', ' ')} limits."
        explanation_hindi = f"{round(safe_serving_g)}g tak hi khao, {limiting_nutrient.replace('_', ' ')} ke liye."

    return {
        "recommended_serving_g": round(safe_serving_g),
        "limiting_factor": limiting_nutrient,
        "servings_per_package": round(package_size_g / safe_serving_g, 1) if safe_serving_g > 0 else 1,
        "daily_percentages": daily_percentages,
        "explanation": explanation,
        "explanation_hindi": explanation_hindi
    }


def process_product(product: dict) -> dict:
    """
    Process a single product and add/update FoodAtEase score data.
    """
    nutrients = product.get("nutrients", {})
    package_size = product.get("package_size_g", 100)

    # Calculate INR score
    inr_score, baseline, modifying = calculate_inr_score(nutrients)
    stars = score_to_stars(inr_score)
    grade = score_to_grade(stars)
    limiting_factors = get_limiting_factors(nutrients)

    # Update foodatease_score
    product["foodatease_score"] = {
        "stars": stars,
        "grade": grade,
        "inr_score": inr_score,
        "baseline_points": baseline,
        "modifying_points": modifying,
        "limiting_factors": limiting_factors
    }

    # Calculate safe limit
    product["safe_limit"] = calculate_safe_limit(nutrients, package_size)

    return product


def main():
    """Main entry point."""
    # Determine input/output files
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    if len(sys.argv) >= 2:
        input_file = Path(sys.argv[1])
    else:
        input_file = project_root / "src" / "data" / "products.json"

    if len(sys.argv) >= 3:
        output_file = Path(sys.argv[2])
    else:
        output_file = input_file  # In-place update

    print(f"Reading products from: {input_file}")

    # Load products
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])
    print(f"Found {len(products)} products")

    # Process each product
    for i, product in enumerate(products):
        product = process_product(product)
        products[i] = product
        print(f"  Processed: {product['name']} -> {product['foodatease_score']['stars']} stars ({product['foodatease_score']['grade']})")

    # Save results
    data["products"] = products

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nSaved updated products to: {output_file}")
    print("Done!")


if __name__ == "__main__":
    main()
