import httpx
from typing import List, Dict, Any

PRODUCTS = None  # Global cache

SUPER_CATEGORIES = {
    "electronics": ["smartphones", "laptops", "tablets", "mobile-accessories"],
    "fashion": ["mens-shirts", "mens-shoes", "mens-watches", "womens-bags", "womens-dresses", "womens-jewellery", "womens-shoes", "womens-watches", "tops", "sunglasses"],
    "beauty": ["beauty", "fragrances", "skin-care"]
}

async def get_all_products() -> List[Dict[str, Any]]:
    """
    Fetch all products from DummyJSON API asynchronously, with caching.
    """
    global PRODUCTS
    if PRODUCTS is None:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://dummyjson.com/products?limit=0")
            response.raise_for_status()
            data = response.json()
            PRODUCTS = data["products"]
    return PRODUCTS

def get_products_by_name(products: List[Dict[str, Any]], name: str) -> List[Dict[str, Any]]:
    """
    Fuzzy match products by title containing the name (case-insensitive).
    """
    lower_name = name.lower()
    return [p for p in products if lower_name in p["title"].lower()]

def get_products_by_category(products: List[Dict[str, Any]], category: str) -> List[Dict[str, Any]]:
    """
    Filter products by category, handling super-categories.
    """
    lower_category = category.lower()
    if lower_category in SUPER_CATEGORIES:
        sub_categories = [sub.lower() for sub in SUPER_CATEGORIES[lower_category]]
        return [p for p in products if p["category"].lower() in sub_categories]
    else:
        return [p for p in products if lower_category in p["category"].lower()]


def get_products_by_rating(products: List[Dict[str, Any]], threshold: float, direction: str = "above") -> List[Dict[str, Any]]:
    """
    Filter products based on rating threshold and direction.
    """
    if direction == "above":
        return [p for p in products if p["rating"] > threshold]
    elif direction == "below":
        return [p for p in products if p["rating"] < threshold]
    elif direction == "equal":
        return [p for p in products if p["rating"] == threshold]
    else:
        return []  # Fallback