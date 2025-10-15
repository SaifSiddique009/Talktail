from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    message: str = Field(..., description="Customer's message to the chatbot", min_length=1)
    groq_api_key: Optional[str] = Field(None, description="User's Groq API key (required on cloud, optional locally if in .env)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Tell me more about Kiwi"
            }
        }

class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str = Field(..., description="Chatbot's natural-language response")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Kiwi is a nutrient-rich fruit priced at $2.49, rated 4.93 stars. It ships overnight and comes with a 6-month warranty."
            }
        }

class Product(BaseModel):
    """Product model based on DummyJSON schema"""
    id: int = Field(..., description="Unique product ID")
    title: str = Field(..., description="Product title")
    description: str = Field(..., description="Product description")
    category: str = Field(..., description="Product category")
    price: float = Field(..., description="Product price")
    discountPercentage: Optional[float] = Field(None, description="Discount percentage")
    rating: Optional[float] = Field(None, description="Average rating")
    stock: Optional[int] = Field(None, description="Stock quantity")
    tags: Optional[List[str]] = Field([], description="Product tags")
    brand: Optional[str] = Field(None, description="Product brand")
    warrantyInformation: Optional[str] = Field(None, description="Warranty details")
    shippingInformation: Optional[str] = Field(None, description="Shipping details")
    availabilityStatus: Optional[str] = Field(None, description="Availability status")
    reviews: Optional[List[Dict[str, Any]]] = Field([], description="List of reviews (each with rating, comment, date, reviewerName, reviewerEmail)")
    returnPolicy: Optional[str] = Field(None, description="Return policy")
    minimumOrderQuantity: Optional[int] = Field(None, description="Minimum order quantity")
    thumbnail: Optional[str] = Field(None, description="Thumbnail URL")
    images: Optional[List[str]] = Field([], description="List of image URLs")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 30,
                "title": "Kiwi",
                "description": "Nutrient-rich kiwi fruit, a tangy addition to your fruit bowl",
                "category": "groceries",
                "price": 2.49,
                "discountPercentage": 15.22,
                "rating": 4.93,
                "stock": 99,
                "tags": ["fruits"],
                "brand": "KiwiCo",
                "warrantyInformation": "6 months warranty",
                "shippingInformation": "Ships overnight",
                "availabilityStatus": "In Stock",
                "reviews": [{"rating": 5, "comment": "Highly recommended!", "date": "2024-05-23T08:56:21.618Z", "reviewerName": "Emily Brown", "reviewerEmail": "emily.brown@x.dummyjson.com"}],
                "returnPolicy": "7 days return policy",
                "minimumOrderQuantity": 1,
                "thumbnail": "https://cdn.dummyjson.com/products/images/groceries/Kiwi/thumbnail.png",
                "images": ["https://cdn.dummyjson.com/products/images/groceries/Kiwi/1.png"]
            }
        }

class ProductsResponse(BaseModel):
    """Response model for products endpoint"""
    products: List[Product] = Field(..., description="List of products")
    total: int = Field(..., description="Total number of products")
    skip: int = Field(..., description="Number of skipped products (0 for all)")
    limit: int = Field(..., description="Limit applied (0 for all)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "products": [{"id": 1, "title": "Essence Mascara Lash Princess"}],  # Truncated
                "total": 194,
                "skip": 0,
                "limit": 0
            }
        }