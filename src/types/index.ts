/**
 * FoodAtEase Type Definitions
 * Core data structures for the Indian packaged food health rating platform
 */

// ============================================================================
// NUTRIENTS
// ============================================================================

export interface Nutrients {
  energy_kcal: number;
  protein_g: number;
  carbohydrates_g: number;
  sugars_g: number;
  added_sugars_g?: number;
  fat_g: number;
  saturated_fat_g: number;
  trans_fat_g?: number;
  fiber_g: number;
  sodium_mg: number;
  cholesterol_mg?: number;

  // Optional micronutrients
  calcium_mg?: number;
  iron_mg?: number;
  vitamin_a_mcg?: number;
  vitamin_c_mg?: number;
  vitamin_d_mcg?: number;
}

// ============================================================================
// INGREDIENTS & ADDITIVES
// ============================================================================

export interface Additive {
  code: string;                       // INS 621, E621
  name: string;                       // Monosodium Glutamate
  name_hindi?: string;                // MSG / अजीनोमोटो
  category: 'preservative' | 'color' | 'flavor' | 'emulsifier' | 'antioxidant' | 'other';
  concern_level: 'safe' | 'caution' | 'avoid';
  banned_in?: string[];               // ['EU', 'USA', 'Japan']
  description: string;
  description_hindi?: string;
}

export interface IngredientFlag {
  type: 'hidden_sugar' | 'banned_additive' | 'ultra_processed' | 'allergen' | 'high_sodium' | 'trans_fat';
  severity: 'info' | 'warning' | 'critical';
  message: string;
  message_hindi?: string;
}

export interface IngredientAnalysis {
  primary_ingredients: string[];      // Top 3-5 ingredients
  hidden_sugars: string[];            // Maltodextrin, corn syrup, etc.
  additives: Additive[];
  allergens: string[];
  flags: IngredientFlag[];
}

// ============================================================================
// FOODATEASE SCORE
// ============================================================================

export type Grade = 'A' | 'B' | 'C' | 'D' | 'F';

export interface FoodAtEaseScore {
  stars: number;                      // 0.5 to 5, in 0.5 increments
  baseline_points: number;            // Bad stuff score (energy, sugar, sodium, sat fat)
  modifying_points: number;           // Good stuff score (protein, fiber)
  final_score: number;                // baseline - modifying
  limiting_factors: string[];         // What's bringing the score down
  grade: Grade;
  summary: string;                    // One-line summary in English
  summary_hindi?: string;             // One-line summary in Hindi
}

// ============================================================================
// SAFE LIMIT
// ============================================================================

export interface SafeLimit {
  max_daily_g: number;                // Maximum grams per day
  recommended_serving_g: number;      // Safe single serving
  servings_per_package: number;       // How many safe servings in package
  limiting_nutrient: string;          // What you hit first (sodium, sugar, etc.)
  explanation: string;                // English explanation
  explanation_hindi?: string;         // Hindi explanation
  daily_percentages: {                // At recommended serving
    sodium: number;
    sugar: number;
    saturated_fat: number;
    calories: number;
  };
}

// ============================================================================
// ROAST / VERDICT
// ============================================================================

export interface Roast {
  text: string;                       // The roast in English
  text_hindi: string;                 // The roast in Hindi/Local language
  tone: 'witty' | 'stern' | 'sympathetic';
  generated_by: 'ai' | 'human';
  approved: boolean;                  // Has been human-reviewed
}

// ============================================================================
// ALTERNATIVES
// ============================================================================

export interface Alternative {
  product_slug?: string;              // If in our database
  name: string;
  type: 'product' | 'homemade' | 'category';
  reason: string;
  comparison?: string;                // "70% less sodium", "3x more protein"
}

// ============================================================================
// PRODUCT (Main Entity)
// ============================================================================

export type NOVAGroup = 1 | 2 | 3 | 4;
export type DataSource = 'label' | 'off' | 'ai_extracted';

export interface Product {
  id: string;
  slug: string;
  name: string;
  name_hindi?: string;
  brand: string;
  brand_slug: string;
  category: string;
  category_slug: string;
  subcategory?: string;
  serving_size_g: number;
  package_size_g: number;
  price_inr?: number;
  barcode?: string;
  image_url?: string;

  // Nutrition per 100g
  nutrients: Nutrients;

  // Ingredients
  ingredients: string[];
  ingredients_analysis: IngredientAnalysis;

  // FoodAtEase Ratings
  foodatease_score: FoodAtEaseScore;
  safe_limit: SafeLimit;
  roast: Roast;

  // Alternatives
  alternatives: Alternative[];

  // Metadata
  nova_group: NOVAGroup;
  verified: boolean;
  last_updated: string;               // ISO date string
  data_source: DataSource;
}

// ============================================================================
// CATEGORY
// ============================================================================

export interface Category {
  slug: string;
  name: string;
  name_hindi: string;
  description: string;
  description_hindi?: string;
  icon: string;                       // Emoji
  parent?: string;                    // For subcategories
  product_count?: number;
}

// ============================================================================
// BRAND
// ============================================================================

export interface Brand {
  slug: string;
  name: string;
  parent_company?: string;
  country: string;
  logo_url?: string;
  product_count?: number;
  average_score?: number;
}

// ============================================================================
// EDUCATIONAL CONTENT
// ============================================================================

export interface EducationalTopic {
  slug: string;
  title: string;
  title_hindi: string;
  description: string;
  description_hindi?: string;
  content: string;                    // Markdown content
  related_products?: string[];        // Product slugs for examples
}

// ============================================================================
// DATA FILE TYPES
// ============================================================================

export interface ProductsData {
  products: Product[];
  last_updated: string;
  total_count: number;
}

export interface CategoriesData {
  categories: Category[];
}

export interface BrandsData {
  brands: Brand[];
}

export interface AdditivesData {
  additives: Additive[];
}

// ============================================================================
// UTILITY TYPES
// ============================================================================

export type NutrientStatus = 'ok' | 'moderate' | 'high' | 'critical';

export interface NutrientThresholds {
  ok: number;
  moderate: number;
  high: number;
}

// Helper type for search results
export interface SearchResult {
  slug: string;
  name: string;
  brand: string;
  category: string;
  stars: number;
  image_url?: string;
}
