from fastapi import APIRouter, Depends
from app.models.schemas import ChatRequest
from app.services.chatbot_service import get_chat_response
from app.services.product_service import get_all_products

router = APIRouter(prefix="/api", tags=["chatbot"])

@router.get("/products")
async def get_products():
    """
    Fetch and return all product data from DummyJSON.
    """
    products = await get_all_products()
    return {"products": products, "total": len(products)}

@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint: Send a message, get an intelligent response about products.
    """
    response = await get_chat_response(request.message, request.groq_api_key)
    return {"response": response}