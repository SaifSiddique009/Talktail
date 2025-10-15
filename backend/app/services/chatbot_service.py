import json, os
from typing import Dict, Any, Optional, List
from app.utils.groq_client import GroqClient
from app.services.product_service import get_all_products, get_products_by_name, get_products_by_category, get_products_by_rating
from app.core.config import settings

# Exclude to save tokens
EXCLUDE_FIELDS = ['meta', 'images', 'thumbnail', 'sku', 'weight', 'dimensions', 'shippingInformation']  

async def get_chat_response(message: str, groq_api_key: Optional[str] = None) -> str:
    api_key = groq_api_key or settings.groq_api_key or os.environ.get('GROQ_API_KEY')
    if not api_key:
        raise ValueError("Groq API key is required.")
    client = GroqClient(api_key)
    
    # Step 1: Analyze query with Groq for intent and params
    analysis_prompt = f"""Analyze the following customer query about products and extract the key information.

Possible intents: 'product_details', 'product_price', 'product_reviews', 'list_by_category', 'list_by_rating', 'list_categories', 'general'.

Extract:
- intent: one of the above (e.g., 'product_price' for price questions, 'list_categories' for asking about available categories)
- product_name: specific product mentioned (if any, e.g., 'Kiwi' or 'Volleyball'), empty string if none
- category: category mentioned (if any, e.g., 'electronics' or 'beauty'), empty string if none
- rating_threshold: number greater than 0 if 'list_by_rating' (e.g., 4 from 'above 4', 3 from 'below 3'), else 0
- rating_direction: 'above', 'below', or 'equal' for rating queries (default 'above' if unspecified), empty string otherwise

Examples:
- Query: "Tell me the reviews for Kiwi." -> {{"intent": "product_reviews", "product_name": "Kiwi", "category": "", "rating_threshold": 0, "rating_direction": ""}}
- Query: "Show me products with ratings above 4." -> {{"intent": "list_by_rating", "product_name": "", "category": "", "rating_threshold": 4, "rating_direction": "above"}}
- Query: "Show products with poor rating below 3." -> {{"intent": "list_by_rating", "product_name": "", "category": "", "rating_threshold": 3, "rating_direction": "below"}}
- Query: "Products with exactly 4.5 rating." -> {{"intent": "list_by_rating", "product_name": "", "category": "", "rating_threshold": 4.5, "rating_direction": "equal"}}
- Query: "Do you have any electronics?" -> {{"intent": "list_by_category", "product_name": "", "category": "electronics", "rating_threshold": 0, "rating_direction": ""}}
- Query: "What category products do you have?" -> {{"intent": "list_categories", "product_name": "", "category": "", "rating_threshold": 0, "rating_direction": ""}}
- Query: "What's the price of kiwi?" -> {{"intent": "product_price", "product_name": "kiwi", "category": "", "rating_threshold": 0, "rating_direction": ""}}

Query: {message}

Output ONLY the valid JSON object in this exact format: {{"intent": "str", "product_name": "str", "category": "str", "rating_threshold": 0, "rating_direction": "str"}}
No additional text, explanations, or formatting—just the JSON."""
    
    analysis_response = client.generate(analysis_prompt, system="You are a JSON extraction tool. Respond with ONLY valid JSON as instructed, no other text.", temperature=0.5)
    
    try:
        analysis_data: Dict[str, Any] = json.loads(analysis_response)
    except json.JSONDecodeError:
        retry_prompt = analysis_prompt + "\n\nIMPORTANT: Output ONLY the JSON now."
        analysis_response = client.generate(retry_prompt, system="You are a JSON extraction tool. Respond with ONLY valid JSON as instructed, no other text.", temperature=0.5)
        try:
            analysis_data = json.loads(analysis_response)
        except json.JSONDecodeError:
            analysis_data = {"intent": "general", "product_name": "", "category": "", "rating_threshold": 0, "rating_direction": ""}

    # Step 2: Fetch products (cached)
    products = await get_all_products()

# Step 3: Retrieve relevant data based on analysis
    relevant_products: List[Dict[str, Any]] = []
    data_str = ""
    if analysis_data["intent"] == "list_categories":
        unique_categories = sorted(set(p["category"] for p in products))
        data_str = json.dumps(unique_categories)
    else:
        if analysis_data["product_name"]:
            relevant_products = get_products_by_name(products, analysis_data["product_name"])
        elif analysis_data["category"]:
            relevant_products = get_products_by_category(products, analysis_data["category"])
        elif analysis_data["rating_threshold"] > 0:
            direction = analysis_data.get("rating_direction", "above")  # Default to above
            relevant_products = get_products_by_rating(products, analysis_data["rating_threshold"], direction)
        
        # Exclude fields and limit to 5
        relevant_products = relevant_products[:5]
        for p in relevant_products:
            for field in EXCLUDE_FIELDS:
                p.pop(field, None)
        data_str = json.dumps(relevant_products, indent=2, default=str)

# Step 4: Intent-specific response prompt
    base_prompt = f"""You are a friendly customer service rep for an online store.

Customer asked: {message}

Base response ONLY on the provided data. Do not invent details. If data is empty, say: "Sorry, I couldn't find any matching products. Try another query?"
Be concise, natural, human-like. End with a question if appropriate.

Data:
{data_str}
"""
    if analysis_data["intent"] == "product_reviews":
        response_prompt = base_prompt + """
- Respond with ONLY the overall rating and 1-2 sample reviews (quote them with reviewer name if available).
- Example: "The Kiwi has a 4.93 rating. Reviews: 'Highly recommended!' - Emily Brown. 'Fast shipping!' - Nora Russell."
"""
    elif analysis_data["intent"] == "list_by_rating":
        response_prompt = base_prompt + """
- List 3-5 products with ONLY their category, name, and rating.
- Mention the filter (e.g., 'Showing products rated {analysis_data['rating_direction']} {analysis_data['rating_threshold']}').
- Format as bullet points: "- [Category]: [Title] (Rating: [rating])"
"""
    elif analysis_data["intent"] == "product_price":
        response_prompt = base_prompt + """
- Respond with ONLY the price. If discountPercentage >0, mention discounted price.
- Example: "The Kiwi is priced at $2.49 (15.22% discount applied)."
"""
    elif analysis_data["intent"] == "list_categories":
        response_prompt = base_prompt + """
- List all unique categories in a simple bulleted list.
- Example: "- Beauty\n- Electronics (includes smartphones, laptops, etc.)\n..."
"""
    elif analysis_data["intent"] == "list_by_category":
        response_prompt = base_prompt + """
- List 3-5 products with name, brief description (from data), price, and rating.
- Use bullets.
"""
    else:  # product_details or general
        response_prompt = base_prompt + """
- For details: Mention title, description, price (with discount if any), rating, brand, tags, warranty, shipping, availability, return policy.
- Keep to 1-2 sentences.
"""

    response = client.generate(response_prompt, system="Follow instructions precisely. Base on data only.", temperature=0.5)
    return response